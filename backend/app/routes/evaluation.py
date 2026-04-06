import json
import logging
from fastapi import APIRouter, Depends, HTTPException, UploadFile, File, Form
from sqlalchemy.orm import Session
from app.database.db import get_db
from app.database.models import Student, TestSession, StudentAnswer, EvaluationReport
from app.services import gemini_service, upload_service
from app.utils.cbse_constants import get_grade

logger = logging.getLogger(__name__)
router = APIRouter(prefix="/evaluation", tags=["evaluation"])


@router.post("/evaluate/{test_id}")
async def evaluate_test(test_id: str, db: Session = Depends(get_db)):
    """Trigger AI evaluation for an already-submitted test."""
    test = db.query(TestSession).filter(TestSession.id == test_id).first()
    if not test:
        raise HTTPException(status_code=404, detail="Test not found")
    if test.status not in ("submitted", "in_progress"):
        raise HTTPException(status_code=400, detail=f"Test status is '{test.status}'. Must be submitted.")

    student = db.query(Student).filter(Student.id == test.student_id).first()
    answers_db = db.query(StudentAnswer).filter(StudentAnswer.test_id == test_id).all()
    answers_map = {a.question_id: a.answer_text for a in answers_db}

    sections = json.loads(test.sections)
    qa_pairs = []
    for section in sections:
        for q in section.get("questions", []):
            qa_pairs.append({
                "question_id": q["id"],
                "question": q["question"],
                "type": q["type"],
                "marks": q["marks"],
                "topic": q.get("topic", ""),
                "expected_answer": q.get("expected_answer", ""),
                "student_answer": answers_map.get(q["id"], "[Not answered]"),
            })

    try:
        eval_result = gemini_service.evaluate_answers(
            class_level=test.class_level,
            subject=test.subject,
            questions_with_answers=qa_pairs,
        )
    except Exception as e:
        logger.error(f"Evaluation failed: {e}")
        raise HTTPException(status_code=502, detail=f"Evaluation failed: {str(e)}")

    # Update per-question scores
    for q_eval in eval_result.get("question_evaluations", []):
        ans = db.query(StudentAnswer).filter(
            StudentAnswer.test_id == test_id,
            StudentAnswer.question_id == q_eval["question_id"],
        ).first()
        if ans:
            ans.score_awarded = q_eval.get("marks_awarded", 0)
            ans.ai_feedback = q_eval.get("feedback", "")

    total_score = eval_result.get("total_score", 0)
    max_score = eval_result.get("max_score", test.total_marks)
    percentage = (total_score / max_score * 100) if max_score else 0
    grade = get_grade(percentage)

    # Build topic scores list
    topic_analysis = eval_result.get("topic_analysis", {})
    topic_scores = [
        {"topic": t, "score": v["score"], "max_score": v["max"], "percentage": v["percentage"]}
        for t, v in topic_analysis.items()
    ]

    # Generate improvement plan
    weak_topics = [ts["topic"] for ts in topic_scores if ts["percentage"] < 50]
    try:
        improvement_plan = gemini_service.generate_improvement_plan(
            class_level=test.class_level,
            subject=test.subject,
            weak_topics=weak_topics,
            evaluation_data=eval_result,
        )
    except Exception:
        improvement_plan = {}

    # Build question feedback list
    qf_list = []
    for q_eval in eval_result.get("question_evaluations", []):
        orig_q = next((q for s in sections for q in s.get("questions", []) if q["id"] == q_eval["question_id"]), {})
        qf_list.append({
            "question_id": q_eval["question_id"],
            "question_text": orig_q.get("question", ""),
            "student_answer": q_eval.get("student_answer", ""),
            "expected_answer": orig_q.get("expected_answer", ""),
            "marks_awarded": q_eval.get("marks_awarded", 0),
            "max_marks": orig_q.get("marks", 0),
            "feedback": q_eval.get("feedback", ""),
            "error_type": q_eval.get("error_type", ""),
        })

    # Persist or update evaluation report
    existing_report = db.query(EvaluationReport).filter(EvaluationReport.test_id == test_id).first()
    if existing_report:
        report = existing_report
    else:
        report = EvaluationReport(test_id=test_id, student_id=test.student_id)
        db.add(report)

    report.total_score = total_score
    report.max_score = max_score
    report.percentage = percentage
    report.grade = grade
    report.topic_scores = json.dumps(topic_scores)
    report.question_feedback = json.dumps(qf_list)
    report.strengths = json.dumps(eval_result.get("strengths", []))
    report.weaknesses = json.dumps(eval_result.get("weaknesses", []))
    report.recommendations = json.dumps(eval_result.get("overall_feedback", "").split(". "))
    report.improvement_plan = json.dumps(improvement_plan)

    test.status = "evaluated"
    db.commit()
    db.refresh(report)

    return {"message": "Evaluation complete", "report_id": report.id, "test_id": test_id}


@router.post("/upload-scan")
async def upload_and_evaluate(
    test_id: str = Form(...),
    student_id: str = Form(...),
    file: UploadFile = File(...),
    db: Session = Depends(get_db),
):
    """Upload a scanned answer sheet, extract text via OCR, store answers, then evaluate."""
    test = db.query(TestSession).filter(TestSession.id == test_id).first()
    if not test:
        raise HTTPException(status_code=404, detail="Test not found")

    filepath, mime_type = await upload_service.save_uploaded_file(file, subfolder="scans")

    # Extract text from image using Gemini Vision
    raw_bytes = upload_service.read_file_bytes(filepath)
    try:
        extracted_text = gemini_service.extract_text_from_image(raw_bytes, mime_type)
    except Exception as e:
        logger.error(f"OCR failed: {e}")
        extracted_text = ""

    # Store extracted text as a single "scan" answer
    scan_answer = StudentAnswer(
        test_id=test_id,
        question_id="scan_upload",
        answer_text=extracted_text,
        uploaded_file_path=filepath,
    )
    db.add(scan_answer)

    # Parse extracted text into per-question answers
    if extracted_text:
        import re
        pattern = re.findall(r"Q(\d+)[:\s]+(.+?)(?=Q\d+[:\s]|$)", extracted_text, re.DOTALL)
        sections = json.loads(test.sections)
        all_questions = [q for s in sections for q in s.get("questions", [])]

        for q_num_str, answer_text in pattern:
            q_num = int(q_num_str) - 1
            if 0 <= q_num < len(all_questions):
                q = all_questions[q_num]
                existing = db.query(StudentAnswer).filter(
                    StudentAnswer.test_id == test_id,
                    StudentAnswer.question_id == q["id"],
                ).first()
                if existing:
                    existing.answer_text = answer_text.strip()
                else:
                    db.add(StudentAnswer(
                        test_id=test_id,
                        question_id=q["id"],
                        answer_text=answer_text.strip(),
                    ))

    test.status = "submitted"
    db.commit()

    return {
        "message": "Answer sheet uploaded and processed",
        "test_id": test_id,
        "extracted_answers_count": len(pattern) if extracted_text else 0,
        "next_step": f"POST /api/v1/evaluation/evaluate/{test_id}",
    }

import json
import logging
from datetime import datetime
from fastapi import APIRouter, Depends, HTTPException
from fastapi.responses import FileResponse
from sqlalchemy.orm import Session
from app.database.db import get_db
from app.database.models import Student, DiagnosticSession, TestSession
from app.schemas.schemas import (
    TestGenerationRequest,
    TestSessionResponse,
    TestStartResponse,
    Section,
    Question,
    QuestionOption,
    BulkAnswerSubmit,
)
from app.services import gemini_service, rag_service, pdf_service
from app.utils.cbse_constants import PAPER_STRUCTURE, MARKS_TO_DURATION, get_topics_for_subject

logger = logging.getLogger(__name__)
router = APIRouter(prefix="/tests", tags=["tests"])


@router.post("/generate", response_model=TestSessionResponse, status_code=201)
def generate_test(payload: TestGenerationRequest, db: Session = Depends(get_db)):
    student = db.query(Student).filter(Student.id == payload.student_id).first()
    if not student:
        raise HTTPException(status_code=404, detail="Student not found")

    # Fetch latest diagnostic for subject
    diagnostic = (
        db.query(DiagnosticSession)
        .filter(
            DiagnosticSession.student_id == payload.student_id,
            DiagnosticSession.subject == payload.subject,
            DiagnosticSession.status == "completed",
        )
        .order_by(DiagnosticSession.created_at.desc())
        .first()
    )

    weak_topics = json.loads(diagnostic.weak_topics or "[]") if diagnostic else []
    strong_topics = json.loads(diagnostic.strong_topics or "[]") if diagnostic else []
    total_marks = payload.total_marks if payload.total_marks in (40, 80) else 80

    # Retrieve RAG context
    topics_to_query = weak_topics or get_topics_for_subject(student.class_level, payload.subject)[:4]
    rag_context = rag_service.query_context(
        class_level=student.class_level,
        subject=payload.subject,
        topics=topics_to_query,
    )

    paper_structure = PAPER_STRUCTURE[total_marks]
    duration = MARKS_TO_DURATION[total_marks]

    # Generate via Gemini
    try:
        test_data = gemini_service.generate_mock_test(
            class_level=student.class_level,
            subject=payload.subject,
            weak_topics=weak_topics,
            strong_topics=strong_topics,
            total_marks=total_marks,
            rag_context=rag_context,
            paper_structure=paper_structure,
        )
    except Exception as e:
        logger.error(f"Gemini test generation failed: {e}")
        raise HTTPException(status_code=502, detail=f"AI generation failed: {str(e)}")

    # Persist test session
    test = TestSession(
        student_id=payload.student_id,
        subject=payload.subject,
        class_level=student.class_level,
        total_marks=total_marks,
        duration_minutes=duration,
        sections=json.dumps(test_data.get("sections", [])),
        status="generated",
    )
    db.add(test)
    db.commit()
    db.refresh(test)

    return _build_response(test)


@router.get("/{test_id}", response_model=TestSessionResponse)
def get_test(test_id: str, db: Session = Depends(get_db)):
    test = db.query(TestSession).filter(TestSession.id == test_id).first()
    if not test:
        raise HTTPException(status_code=404, detail="Test not found")
    return _build_response(test)


@router.post("/{test_id}/start", response_model=TestStartResponse)
def start_test(test_id: str, db: Session = Depends(get_db)):
    test = db.query(TestSession).filter(TestSession.id == test_id).first()
    if not test:
        raise HTTPException(status_code=404, detail="Test not found")
    if test.status == "submitted":
        raise HTTPException(status_code=400, detail="Test already submitted")

    if test.status == "generated":
        test.status = "in_progress"
        test.started_at = datetime.utcnow()
        db.commit()

    sections = json.loads(test.sections)
    total_questions = sum(len(s.get("questions", [])) for s in sections)

    return TestStartResponse(
        test_id=test.id,
        duration_minutes=test.duration_minutes,
        total_questions=total_questions,
        total_marks=test.total_marks,
        started_at=test.started_at or datetime.utcnow(),
    )


@router.get("/{test_id}/download-pdf")
def download_test_pdf(test_id: str, db: Session = Depends(get_db)):
    test = db.query(TestSession).filter(TestSession.id == test_id).first()
    if not test:
        raise HTTPException(status_code=404, detail="Test not found")

    student = db.query(Student).filter(Student.id == test.student_id).first()
    filename = f"test_{test_id}.pdf"

    # Generate PDF if not already cached
    if not test.pdf_path:
        sections_data = json.loads(test.sections)
        test_data = {
            "class_level": test.class_level,
            "subject": test.subject,
            "total_marks": test.total_marks,
            "duration_minutes": test.duration_minutes,
            "sections": sections_data,
        }
        filepath = pdf_service.generate_question_paper(
            test_session_data=test_data,
            student_name=student.name,
            output_filename=filename,
        )
        test.pdf_path = filepath
        db.commit()

    return FileResponse(
        path=test.pdf_path,
        media_type="application/pdf",
        filename=f"BoardAI_MockTest_{test.subject}_{test_id[:8]}.pdf",
    )


@router.post("/{test_id}/submit")
def submit_test(test_id: str, payload: BulkAnswerSubmit, db: Session = Depends(get_db)):
    test = db.query(TestSession).filter(TestSession.id == test_id).first()
    if not test:
        raise HTTPException(status_code=404, detail="Test not found")
    if test.status == "submitted":
        raise HTTPException(status_code=400, detail="Test already submitted")

    # Store answers as JSON on the test for simplicity
    # In production, use StudentAnswer table per question
    from app.database.models import StudentAnswer
    for qid, answer in payload.answers.items():
        existing = (
            db.query(StudentAnswer)
            .filter(StudentAnswer.test_id == test_id, StudentAnswer.question_id == qid)
            .first()
        )
        if existing:
            existing.answer_text = answer
        else:
            db.add(StudentAnswer(test_id=test_id, question_id=qid, answer_text=answer))

    test.status = "submitted"
    test.submitted_at = datetime.utcnow()
    db.commit()

    return {"message": "Test submitted successfully", "test_id": test_id}


@router.get("/student/{student_id}")
def get_student_tests(student_id: str, db: Session = Depends(get_db)):
    tests = (
        db.query(TestSession)
        .filter(TestSession.student_id == student_id)
        .order_by(TestSession.created_at.desc())
        .all()
    )
    return [
        {
            "id": t.id,
            "subject": t.subject,
            "class_level": t.class_level,
            "total_marks": t.total_marks,
            "duration_minutes": t.duration_minutes,
            "status": t.status,
            "created_at": t.created_at,
            "submitted_at": t.submitted_at,
        }
        for t in tests
    ]


def _build_response(test: TestSession) -> TestSessionResponse:
    raw_sections = json.loads(test.sections)
    sections = []
    for sec in raw_sections:
        questions = []
        for q in sec.get("questions", []):
            opts = None
            if q.get("options"):
                opts = [QuestionOption(label=o["label"], text=o["text"]) for o in q["options"]]
            questions.append(
                Question(
                    id=q["id"],
                    type=q["type"],
                    question=q["question"],
                    marks=q["marks"],
                    topic=q.get("topic", ""),
                    chapter=q.get("chapter"),
                    difficulty=q.get("difficulty", "medium"),
                    options=opts,
                    expected_answer=q.get("expected_answer"),
                    hint=q.get("hint"),
                )
            )
        sections.append(
            Section(
                name=sec["name"],
                description=sec.get("description", ""),
                questions=questions,
                total_marks=sec.get("total_marks", 0),
            )
        )
    return TestSessionResponse(
        id=test.id,
        student_id=test.student_id,
        subject=test.subject,
        class_level=test.class_level,
        total_marks=test.total_marks,
        duration_minutes=test.duration_minutes,
        sections=sections,
        status=test.status,
        created_at=test.created_at,
    )

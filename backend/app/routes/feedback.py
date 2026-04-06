import json
import logging
from fastapi import APIRouter, Depends, HTTPException
from fastapi.responses import FileResponse
from sqlalchemy.orm import Session
from app.database.db import get_db
from app.database.models import Student, TestSession, EvaluationReport
from app.schemas.schemas import ReportResponse, TopicScore, QuestionEvaluation, HistoryEntry
from app.services import pdf_service

logger = logging.getLogger(__name__)
router = APIRouter(prefix="/reports", tags=["reports"])


@router.get("/test/{test_id}", response_model=ReportResponse)
def get_report(test_id: str, db: Session = Depends(get_db)):
    report = db.query(EvaluationReport).filter(EvaluationReport.test_id == test_id).first()
    if not report:
        raise HTTPException(status_code=404, detail="Report not found. Ensure test has been evaluated.")

    test = db.query(TestSession).filter(TestSession.id == test_id).first()
    return _build_report_response(report, test)


@router.get("/{report_id}/download-pdf")
def download_report_pdf(report_id: str, db: Session = Depends(get_db)):
    report = db.query(EvaluationReport).filter(EvaluationReport.id == report_id).first()
    if not report:
        raise HTTPException(status_code=404, detail="Report not found")

    student = db.query(Student).filter(Student.id == report.student_id).first()
    test = db.query(TestSession).filter(TestSession.id == report.test_id).first()
    filename = f"report_{report_id}.pdf"

    if not report.report_pdf_path:
        report_data = {
            "total_score": report.total_score,
            "max_score": report.max_score,
            "percentage": report.percentage,
            "grade": report.grade,
            "topic_scores": json.loads(report.topic_scores or "[]"),
            "strengths": json.loads(report.strengths or "[]"),
            "weaknesses": json.loads(report.weaknesses or "[]"),
            "recommendations": json.loads(report.recommendations or "[]"),
        }
        filepath = pdf_service.generate_report_pdf(
            report_data=report_data,
            student_name=student.name,
            subject=test.subject if test else "",
            output_filename=filename,
        )
        report.report_pdf_path = filepath
        db.commit()

    return FileResponse(
        path=report.report_pdf_path,
        media_type="application/pdf",
        filename=f"BoardAI_Report_{test.subject if test else 'Report'}_{report_id[:8]}.pdf",
    )


@router.get("/student/{student_id}")
def get_student_history(student_id: str, db: Session = Depends(get_db)):
    reports = (
        db.query(EvaluationReport, TestSession)
        .join(TestSession, EvaluationReport.test_id == TestSession.id)
        .filter(EvaluationReport.student_id == student_id)
        .order_by(EvaluationReport.created_at.desc())
        .all()
    )
    return [
        HistoryEntry(
            test_id=r.test_id,
            subject=t.subject,
            date=r.created_at,
            score=r.total_score,
            max_score=r.max_score,
            percentage=r.percentage,
            grade=r.grade,
        )
        for r, t in reports
    ]


def _build_report_response(report: EvaluationReport, test: TestSession) -> ReportResponse:
    raw_topic_scores = json.loads(report.topic_scores or "[]")
    topic_scores = [
        TopicScore(
            topic=ts["topic"],
            score=ts["score"],
            max_score=ts["max_score"],
            percentage=ts["percentage"],
        )
        for ts in raw_topic_scores
    ]

    raw_qf = json.loads(report.question_feedback or "[]")
    question_feedback = [
        QuestionEvaluation(
            question_id=qf["question_id"],
            question_text=qf.get("question_text", ""),
            student_answer=qf.get("student_answer", ""),
            expected_answer=qf.get("expected_answer", ""),
            marks_awarded=qf.get("marks_awarded", 0),
            max_marks=qf.get("max_marks", 0),
            feedback=qf.get("feedback", ""),
            error_type=qf.get("error_type"),
        )
        for qf in raw_qf
    ]

    return ReportResponse(
        id=report.id,
        test_id=report.test_id,
        student_id=report.student_id,
        subject=test.subject if test else "",
        total_score=report.total_score,
        max_score=report.max_score,
        percentage=report.percentage,
        grade=report.grade,
        topic_scores=topic_scores,
        question_feedback=question_feedback,
        strengths=json.loads(report.strengths or "[]"),
        weaknesses=json.loads(report.weaknesses or "[]"),
        recommendations=json.loads(report.recommendations or "[]"),
        improvement_plan=json.loads(report.improvement_plan or "{}"),
        created_at=report.created_at,
    )

import json
import logging
from datetime import datetime
from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from app.database.db import get_db
from app.database.models import Student, DiagnosticSession
from app.schemas.schemas import (
    DiagnosticStart,
    DiagnosticQuestionsResponse,
    DiagnosticSubmit,
    DiagnosticResult,
    DiagnosticQuestion,
)
from app.services import gemini_service
from app.utils.cbse_constants import get_diagnostic_questions, get_topics_for_subject

logger = logging.getLogger(__name__)
router = APIRouter(prefix="/diagnostics", tags=["diagnostics"])


@router.post("/start", response_model=DiagnosticQuestionsResponse)
def start_diagnostic(payload: DiagnosticStart, db: Session = Depends(get_db)):
    student = db.query(Student).filter(Student.id == payload.student_id).first()
    if not student:
        raise HTTPException(status_code=404, detail="Student not found")

    subjects = json.loads(student.subjects)
    if payload.subject not in subjects:
        raise HTTPException(status_code=400, detail=f"Subject '{payload.subject}' not in student profile")

    # Create or reuse in-progress session
    existing = (
        db.query(DiagnosticSession)
        .filter(
            DiagnosticSession.student_id == payload.student_id,
            DiagnosticSession.subject == payload.subject,
            DiagnosticSession.status == "in_progress",
        )
        .first()
    )
    if existing:
        session = existing
    else:
        session = DiagnosticSession(
            student_id=payload.student_id,
            subject=payload.subject,
            status="in_progress",
        )
        db.add(session)
        db.commit()
        db.refresh(session)

    raw_questions = get_diagnostic_questions(payload.subject)
    questions = [DiagnosticQuestion(**q) for q in raw_questions]

    return DiagnosticQuestionsResponse(
        session_id=session.id,
        subject=payload.subject,
        questions=questions,
    )


@router.post("/submit", response_model=DiagnosticResult)
def submit_diagnostic(payload: DiagnosticSubmit, db: Session = Depends(get_db)):
    session = db.query(DiagnosticSession).filter(DiagnosticSession.id == payload.session_id).first()
    if not session:
        raise HTTPException(status_code=404, detail="Diagnostic session not found")
    if session.status == "completed":
        raise HTTPException(status_code=400, detail="Diagnostic already submitted")

    student = db.query(Student).filter(Student.id == session.student_id).first()
    all_topics = get_topics_for_subject(student.class_level, session.subject)

    try:
        analysis = gemini_service.analyze_diagnostic_responses(
            class_level=student.class_level,
            subject=session.subject,
            responses=payload.responses,
            all_topics=all_topics,
        )
    except Exception as e:
        logger.error(f"Gemini diagnostic analysis failed: {e}")
        # Fallback: simple analysis based on numeric values
        analysis = _fallback_analysis(payload.responses, all_topics)

    session.responses = json.dumps(payload.responses)
    session.weak_topics = json.dumps(analysis.get("weak_topics", []))
    session.strong_topics = json.dumps(analysis.get("strong_topics", []))
    session.confidence_score = float(analysis.get("confidence_score", 3.0))
    session.status = "completed"
    session.completed_at = datetime.utcnow()
    db.commit()

    return DiagnosticResult(
        session_id=session.id,
        subject=session.subject,
        weak_topics=analysis.get("weak_topics", []),
        strong_topics=analysis.get("strong_topics", []),
        confidence_score=session.confidence_score,
        message=analysis.get(
            "analysis_summary",
            f"Diagnostic for {session.subject} completed. Test will be personalized based on your responses.",
        ),
    )


@router.get("/student/{student_id}")
def get_diagnostics(student_id: str, db: Session = Depends(get_db)):
    sessions = (
        db.query(DiagnosticSession)
        .filter(DiagnosticSession.student_id == student_id, DiagnosticSession.status == "completed")
        .all()
    )
    return [
        {
            "session_id": s.id,
            "subject": s.subject,
            "weak_topics": json.loads(s.weak_topics or "[]"),
            "strong_topics": json.loads(s.strong_topics or "[]"),
            "confidence_score": s.confidence_score,
            "completed_at": s.completed_at,
        }
        for s in sessions
    ]


def _fallback_analysis(responses: dict, all_topics: list) -> dict:
    """Simple rule-based fallback when Gemini is unavailable."""
    scores = {}
    for qid, val in responses.items():
        try:
            num = int(str(val).split(" ")[0].split("–")[0].strip())
            scores[qid] = num
        except (ValueError, AttributeError):
            scores[qid] = 3

    avg = sum(scores.values()) / len(scores) if scores else 3.0
    weak = [t for t in all_topics[:3]] if avg < 3 else []
    strong = [t for t in all_topics[-2:]] if avg >= 4 else []

    return {
        "weak_topics": weak,
        "strong_topics": strong,
        "confidence_score": min(avg, 5.0),
        "analysis_summary": "Diagnostic complete. Your test has been personalized.",
    }

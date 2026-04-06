import uuid
from datetime import datetime
from sqlalchemy import Column, String, Integer, Float, DateTime, Text, ForeignKey, Enum as SAEnum
from sqlalchemy.orm import relationship
from app.database.db import Base


def gen_uuid():
    return str(uuid.uuid4())


class Student(Base):
    __tablename__ = "students"

    id = Column(String, primary_key=True, default=gen_uuid)
    name = Column(String(100), nullable=False)
    class_level = Column(Integer, nullable=False)  # 10 or 12
    subjects = Column(Text, nullable=False)  # JSON-encoded list
    created_at = Column(DateTime, default=datetime.utcnow)

    diagnostics = relationship("DiagnosticSession", back_populates="student", cascade="all, delete")
    tests = relationship("TestSession", back_populates="student", cascade="all, delete")


class DiagnosticSession(Base):
    __tablename__ = "diagnostic_sessions"

    id = Column(String, primary_key=True, default=gen_uuid)
    student_id = Column(String, ForeignKey("students.id"), nullable=False)
    subject = Column(String(50), nullable=False)
    status = Column(SAEnum("in_progress", "completed", name="diag_status"), default="in_progress")
    weak_topics = Column(Text, nullable=True)   # JSON-encoded list
    strong_topics = Column(Text, nullable=True)  # JSON-encoded list
    confidence_score = Column(Float, nullable=True)
    responses = Column(Text, nullable=True)     # JSON-encoded dict
    created_at = Column(DateTime, default=datetime.utcnow)
    completed_at = Column(DateTime, nullable=True)

    student = relationship("Student", back_populates="diagnostics")


class TestSession(Base):
    __tablename__ = "test_sessions"

    id = Column(String, primary_key=True, default=gen_uuid)
    student_id = Column(String, ForeignKey("students.id"), nullable=False)
    subject = Column(String(50), nullable=False)
    class_level = Column(Integer, nullable=False)
    total_marks = Column(Integer, nullable=False)
    duration_minutes = Column(Integer, nullable=False)
    sections = Column(Text, nullable=False)      # JSON-encoded full test
    status = Column(
        SAEnum("generated", "in_progress", "submitted", "evaluated", name="test_status"),
        default="generated",
    )
    pdf_path = Column(String, nullable=True)
    started_at = Column(DateTime, nullable=True)
    submitted_at = Column(DateTime, nullable=True)
    created_at = Column(DateTime, default=datetime.utcnow)

    student = relationship("Student", back_populates="tests")
    answers = relationship("StudentAnswer", back_populates="test", cascade="all, delete")
    evaluation = relationship("EvaluationReport", back_populates="test", uselist=False, cascade="all, delete")


class StudentAnswer(Base):
    __tablename__ = "student_answers"

    id = Column(String, primary_key=True, default=gen_uuid)
    test_id = Column(String, ForeignKey("test_sessions.id"), nullable=False)
    question_id = Column(String, nullable=False)
    answer_text = Column(Text, nullable=True)
    uploaded_file_path = Column(String, nullable=True)
    score_awarded = Column(Float, nullable=True)
    ai_feedback = Column(Text, nullable=True)
    submitted_at = Column(DateTime, default=datetime.utcnow)

    test = relationship("TestSession", back_populates="answers")


class EvaluationReport(Base):
    __tablename__ = "evaluation_reports"

    id = Column(String, primary_key=True, default=gen_uuid)
    test_id = Column(String, ForeignKey("test_sessions.id"), nullable=False, unique=True)
    student_id = Column(String, ForeignKey("students.id"), nullable=False)
    total_score = Column(Float, nullable=False)
    max_score = Column(Integer, nullable=False)
    percentage = Column(Float, nullable=False)
    grade = Column(String(5), nullable=False)
    topic_scores = Column(Text, nullable=True)        # JSON
    question_feedback = Column(Text, nullable=True)   # JSON
    strengths = Column(Text, nullable=True)           # JSON
    weaknesses = Column(Text, nullable=True)          # JSON
    recommendations = Column(Text, nullable=True)     # JSON
    improvement_plan = Column(Text, nullable=True)    # JSON
    report_pdf_path = Column(String, nullable=True)
    created_at = Column(DateTime, default=datetime.utcnow)

    test = relationship("TestSession", back_populates="evaluation")

from pydantic import BaseModel, field_validator
from typing import List, Optional, Dict, Any
from datetime import datetime


# ── Student ──────────────────────────────────────────────────────────────────

class StudentCreate(BaseModel):
    name: str
    class_level: int
    subjects: List[str]

    @field_validator("class_level")
    @classmethod
    def validate_class(cls, v):
        if v not in (10, 12):
            raise ValueError("class_level must be 10 or 12")
        return v

    @field_validator("subjects")
    @classmethod
    def validate_subjects(cls, v):
        if not v:
            raise ValueError("At least one subject is required")
        if len(v) > 6:
            raise ValueError("Maximum 6 subjects allowed")
        return v


class StudentResponse(BaseModel):
    id: str
    name: str
    class_level: int
    subjects: List[str]
    created_at: datetime

    class Config:
        from_attributes = True


# ── Diagnostic ────────────────────────────────────────────────────────────────

class DiagnosticStart(BaseModel):
    student_id: str
    subject: str


class DiagnosticQuestion(BaseModel):
    id: str
    type: str          # confidence | topic_strength | past_performance
    question: str
    options: Optional[List[str]] = None
    topic: Optional[str] = None


class DiagnosticQuestionsResponse(BaseModel):
    session_id: str
    subject: str
    questions: List[DiagnosticQuestion]


class DiagnosticSubmit(BaseModel):
    session_id: str
    responses: Dict[str, Any]  # question_id -> answer value


class DiagnosticResult(BaseModel):
    session_id: str
    subject: str
    weak_topics: List[str]
    strong_topics: List[str]
    confidence_score: float
    message: str


# ── Test ─────────────────────────────────────────────────────────────────────

class QuestionOption(BaseModel):
    label: str
    text: str


class Question(BaseModel):
    id: str
    type: str          # mcq | short_answer | long_answer | case_based
    question: str
    marks: int
    topic: str
    chapter: Optional[str] = None
    difficulty: str    # easy | medium | hard
    options: Optional[List[QuestionOption]] = None
    expected_answer: Optional[str] = None
    hint: Optional[str] = None


class Section(BaseModel):
    name: str
    description: str
    questions: List[Question]
    total_marks: int


class TestGenerationRequest(BaseModel):
    student_id: str
    subject: str
    total_marks: int = 80  # 40 or 80


class TestSessionResponse(BaseModel):
    id: str
    student_id: str
    subject: str
    class_level: int
    total_marks: int
    duration_minutes: int
    sections: List[Section]
    status: str
    created_at: datetime

    class Config:
        from_attributes = True


class TestStartResponse(BaseModel):
    test_id: str
    duration_minutes: int
    total_questions: int
    total_marks: int
    started_at: datetime


# ── Answers ───────────────────────────────────────────────────────────────────

class AnswerSubmit(BaseModel):
    test_id: str
    question_id: str
    answer_text: str


class BulkAnswerSubmit(BaseModel):
    test_id: str
    student_id: str
    answers: Dict[str, str]  # question_id -> answer_text
    time_taken_minutes: Optional[int] = None


# ── Evaluation / Report ───────────────────────────────────────────────────────

class QuestionEvaluation(BaseModel):
    question_id: str
    question_text: str
    student_answer: str
    expected_answer: str
    marks_awarded: float
    max_marks: int
    feedback: str
    error_type: Optional[str] = None  # conceptual | calculation | incomplete | correct


class TopicScore(BaseModel):
    topic: str
    score: float
    max_score: int
    percentage: float


class ReportResponse(BaseModel):
    id: str
    test_id: str
    student_id: str
    subject: str
    total_score: float
    max_score: int
    percentage: float
    grade: str
    topic_scores: List[TopicScore]
    question_feedback: List[QuestionEvaluation]
    strengths: List[str]
    weaknesses: List[str]
    recommendations: List[str]
    improvement_plan: Dict[str, Any]
    created_at: datetime


class HistoryEntry(BaseModel):
    test_id: str
    subject: str
    date: datetime
    score: float
    max_score: int
    percentage: float
    grade: str

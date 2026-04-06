import json
from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from app.database.db import get_db
from app.database.models import Student
from app.schemas.schemas import StudentCreate, StudentResponse
from app.utils.cbse_constants import SUBJECTS_BY_CLASS

router = APIRouter(prefix="/students", tags=["students"])


@router.post("", response_model=StudentResponse, status_code=201)
def create_student(payload: StudentCreate, db: Session = Depends(get_db)):
    valid_subjects = SUBJECTS_BY_CLASS.get(payload.class_level, [])
    invalid = [s for s in payload.subjects if s not in valid_subjects]
    if invalid:
        raise HTTPException(
            status_code=400,
            detail=f"Invalid subjects for Class {payload.class_level}: {invalid}. Valid: {valid_subjects}",
        )

    student = Student(
        name=payload.name,
        class_level=payload.class_level,
        subjects=json.dumps(payload.subjects),
    )
    db.add(student)
    db.commit()
    db.refresh(student)
    return _to_response(student)


@router.get("/{student_id}", response_model=StudentResponse)
def get_student(student_id: str, db: Session = Depends(get_db)):
    student = db.query(Student).filter(Student.id == student_id).first()
    if not student:
        raise HTTPException(status_code=404, detail="Student not found")
    return _to_response(student)


def _to_response(student: Student) -> StudentResponse:
    return StudentResponse(
        id=student.id,
        name=student.name,
        class_level=student.class_level,
        subjects=json.loads(student.subjects),
        created_at=student.created_at,
    )

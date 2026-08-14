from typing import List, Optional, Any
from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session

from app.db.session import get_db
from app.models.grade import Grade
from app.models.student import Student
from app.models.assignment import Assignment
from app.schemas.grade import GradeCreate, GradeUpdate, GradeResponse

router = APIRouter()


@router.get("/", response_model=List[GradeResponse], summary="List grades")
def list_grades(
    student_id: Optional[int] = None,
    assignment_id: Optional[int] = None,
    skip: int = 0,
    limit: int = 100,
    db: Session = Depends(get_db)
) -> Any:
    """List grades with optional filtering by student or assignment."""
    query = db.query(Grade)
    if student_id is not None:
        query = query.filter(Grade.student_id == student_id)
    if assignment_id is not None:
        query = query.filter(Grade.assignment_id == assignment_id)
    return query.offset(skip).limit(limit).all()


@router.post("/", response_model=GradeResponse, status_code=status.HTTP_201_CREATED, summary="Record a grade")
def record_grade(
    grade_in: GradeCreate,
    db: Session = Depends(get_db)
) -> Any:
    """Record a grade for a student assignment."""
    student = db.query(Student).filter(Student.id == grade_in.student_id).first()
    if not student:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Student not found")

    assignment = db.query(Assignment).filter(Assignment.id == grade_in.assignment_id).first()
    if not assignment:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Assignment not found")

    existing_grade = db.query(Grade).filter(
        Grade.assignment_id == grade_in.assignment_id,
        Grade.student_id == grade_in.student_id
    ).first()

    if existing_grade:
        # Update existing grade score
        existing_grade.score = grade_in.score
        if grade_in.feedback is not None:
            existing_grade.feedback = grade_in.feedback
        db.commit()
        db.refresh(existing_grade)
        return existing_grade

    grade = Grade(**grade_in.model_dump())
    db.add(grade)
    db.commit()
    db.refresh(grade)
    return grade


@router.get("/{grade_id}", response_model=GradeResponse, summary="Get grade details")
def get_grade(
    grade_id: int,
    db: Session = Depends(get_db)
) -> Any:
    """Get single grade details."""
    grade = db.query(Grade).filter(Grade.id == grade_id).first()
    if not grade:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Grade not found")
    return grade


@router.put("/{grade_id}", response_model=GradeResponse, summary="Update grade")
def update_grade(
    grade_id: int,
    grade_in: GradeUpdate,
    db: Session = Depends(get_db)
) -> Any:
    """Update grade score or feedback."""
    grade = db.query(Grade).filter(Grade.id == grade_id).first()
    if not grade:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Grade not found")

    update_data = grade_in.model_dump(exclude_unset=True)
    for field, value in update_data.items():
        setattr(grade, field, value)

    db.commit()
    db.refresh(grade)
    return grade


@router.delete("/{grade_id}", status_code=status.HTTP_204_NO_CONTENT, summary="Delete grade")
def delete_grade(
    grade_id: int,
    db: Session = Depends(get_db)
) -> None:
    """Delete a grade record."""
    grade = db.query(Grade).filter(Grade.id == grade_id).first()
    if not grade:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Grade not found")
    db.delete(grade)
    db.commit()

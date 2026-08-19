from typing import List, Optional, Any
from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session

from app.db.session import get_db
from app.models.assignment import Assignment
from app.models.course import Course
from app.models.student import Student
from app.schemas.assignment import AssignmentCreate, AssignmentUpdate, AssignmentResponse
from app.api.deps import get_current_user, get_current_instructor

router = APIRouter()


@router.get("/", response_model=List[AssignmentResponse], summary="List lessons")
def list_assignments(
    course_id: Optional[int] = None,
    skip: int = 0,
    limit: int = 100,
    db: Session = Depends(get_db),
    current_user: Student = Depends(get_current_user),
) -> Any:
    query = db.query(Assignment)
    if course_id is not None:
        query = query.filter(Assignment.course_id == course_id)
    return query.offset(skip).limit(limit).all()


@router.post("/", response_model=AssignmentResponse, status_code=status.HTTP_201_CREATED, summary="Create lesson")
def create_assignment(
    assignment_in: AssignmentCreate,
    db: Session = Depends(get_db),
    current_user: Student = Depends(get_current_instructor),
) -> Any:
    course = db.query(Course).filter(Course.id == assignment_in.course_id).first()
    if not course:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Module not found")

    assignment = Assignment(**assignment_in.model_dump())
    db.add(assignment)
    db.commit()
    db.refresh(assignment)
    return assignment


@router.get("/{assignment_id}", response_model=AssignmentResponse, summary="Get lesson details")
def get_assignment(
    assignment_id: int,
    db: Session = Depends(get_db),
    current_user: Student = Depends(get_current_user),
) -> Any:
    assignment = db.query(Assignment).filter(Assignment.id == assignment_id).first()
    if not assignment:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Lesson not found")
    return assignment


@router.put("/{assignment_id}", response_model=AssignmentResponse, summary="Update lesson")
def update_assignment(
    assignment_id: int,
    assignment_in: AssignmentUpdate,
    db: Session = Depends(get_db),
    current_user: Student = Depends(get_current_instructor),
) -> Any:
    assignment = db.query(Assignment).filter(Assignment.id == assignment_id).first()
    if not assignment:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Lesson not found")

    update_data = assignment_in.model_dump(exclude_unset=True)
    for field, value in update_data.items():
        setattr(assignment, field, value)

    db.commit()
    db.refresh(assignment)
    return assignment


@router.delete("/{assignment_id}", status_code=status.HTTP_204_NO_CONTENT, summary="Delete lesson")
def delete_assignment(
    assignment_id: int,
    db: Session = Depends(get_db),
    current_user: Student = Depends(get_current_instructor),
) -> None:
    assignment = db.query(Assignment).filter(Assignment.id == assignment_id).first()
    if not assignment:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Lesson not found")
    db.delete(assignment)
    db.commit()

from typing import List, Optional, Any
from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session

from app.db.session import get_db
from app.models.assignment import Assignment
from app.models.course import Course
from app.schemas.assignment import AssignmentCreate, AssignmentUpdate, AssignmentResponse

router = APIRouter()


@router.get("/", response_model=List[AssignmentResponse], summary="List assignments")
def list_assignments(
    course_id: Optional[int] = None,
    skip: int = 0,
    limit: int = 100,
    db: Session = Depends(get_db)
) -> Any:
    """Retrieve assignments, optionally filtered by course_id."""
    query = db.query(Assignment)
    if course_id is not None:
        query = query.filter(Assignment.course_id == course_id)
    return query.offset(skip).limit(limit).all()


@router.post("/", response_model=AssignmentResponse, status_code=status.HTTP_201_CREATED, summary="Create assignment")
def create_assignment(
    assignment_in: AssignmentCreate,
    db: Session = Depends(get_db)
) -> Any:
    """Create a new assignment for a course."""
    course = db.query(Course).filter(Course.id == assignment_in.course_id).first()
    if not course:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Course not found")

    assignment = Assignment(**assignment_in.model_dump())
    db.add(assignment)
    db.commit()
    db.refresh(assignment)
    return assignment


@router.get("/{assignment_id}", response_model=AssignmentResponse, summary="Get assignment details")
def get_assignment(
    assignment_id: int,
    db: Session = Depends(get_db)
) -> Any:
    """Get single assignment by ID."""
    assignment = db.query(Assignment).filter(Assignment.id == assignment_id).first()
    if not assignment:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Assignment not found")
    return assignment


@router.put("/{assignment_id}", response_model=AssignmentResponse, summary="Update assignment")
def update_assignment(
    assignment_id: int,
    assignment_in: AssignmentUpdate,
    db: Session = Depends(get_db)
) -> Any:
    """Update assignment details."""
    assignment = db.query(Assignment).filter(Assignment.id == assignment_id).first()
    if not assignment:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Assignment not found")

    update_data = assignment_in.model_dump(exclude_unset=True)
    for field, value in update_data.items():
        setattr(assignment, field, value)

    db.commit()
    db.refresh(assignment)
    return assignment


@router.delete("/{assignment_id}", status_code=status.HTTP_204_NO_CONTENT, summary="Delete assignment")
def delete_assignment(
    assignment_id: int,
    db: Session = Depends(get_db)
) -> None:
    """Delete an assignment."""
    assignment = db.query(Assignment).filter(Assignment.id == assignment_id).first()
    if not assignment:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Assignment not found")
    db.delete(assignment)
    db.commit()

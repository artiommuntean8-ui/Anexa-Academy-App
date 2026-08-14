from typing import List, Any
from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session

from app.db.session import get_db
from app.models.course import Course
from app.models.student import Student
from app.models.enrollment import Enrollment
from app.schemas.course import CourseCreate, CourseUpdate, CourseResponse
from app.schemas.student import StudentResponse
from app.schemas.enrollment import EnrollmentCreate, EnrollmentResponse

router = APIRouter()


@router.get("/", response_model=List[CourseResponse], summary="List all courses")
def list_courses(
    skip: int = 0,
    limit: int = 100,
    db: Session = Depends(get_db)
) -> Any:
    """List available courses."""
    return db.query(Course).offset(skip).limit(limit).all()


@router.post("/", response_model=CourseResponse, status_code=status.HTTP_201_CREATED, summary="Create a new course")
def create_course(
    course_in: CourseCreate,
    db: Session = Depends(get_db)
) -> Any:
    """Create a new course in the curriculum."""
    if db.query(Course).filter(Course.code == course_in.code).first():
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=f"Course with code '{course_in.code}' already exists."
        )
    course = Course(**course_in.model_dump())
    db.add(course)
    db.commit()
    db.refresh(course)
    return course


@router.get("/{course_id}", response_model=CourseResponse, summary="Get course details")
def get_course(
    course_id: int,
    db: Session = Depends(get_db)
) -> Any:
    """Get course by ID."""
    course = db.query(Course).filter(Course.id == course_id).first()
    if not course:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Course not found")
    return course


@router.post("/{course_id}/enroll", response_model=EnrollmentResponse, summary="Enroll student in course")
def enroll_student(
    course_id: int,
    enrollment_in: EnrollmentCreate,
    db: Session = Depends(get_db)
) -> Any:
    """Enroll a student into a course."""
    course = db.query(Course).filter(Course.id == course_id).first()
    if not course:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Course not found")

    student = db.query(Student).filter(Student.id == enrollment_in.student_id).first()
    if not student:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Student not found")

    existing = db.query(Enrollment).filter(
        Enrollment.course_id == course_id,
        Enrollment.student_id == enrollment_in.student_id
    ).first()
    if existing:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Student is already enrolled in this course."
        )

    enrollment = Enrollment(
        course_id=course_id,
        student_id=enrollment_in.student_id,
        status=enrollment_in.status
    )
    db.add(enrollment)
    db.commit()
    db.refresh(enrollment)
    return enrollment


@router.get("/{course_id}/students", response_model=List[StudentResponse], summary="List enrolled students")
def list_enrolled_students(
    course_id: int,
    db: Session = Depends(get_db)
) -> Any:
    """Get list of students enrolled in this course."""
    enrollments = db.query(Enrollment).filter(
        Enrollment.course_id == course_id,
        Enrollment.status == "active"
    ).all()
    student_ids = [e.student_id for e in enrollments]
    if not student_ids:
        return []
    return db.query(Student).filter(Student.id.in_(student_ids)).all()

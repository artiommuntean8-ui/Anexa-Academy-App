from typing import List, Any
from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session

from app.db.session import get_db
from app.models.course import Course
from app.models.student import Student
from app.models.enrollment import Enrollment
from app.schemas.course import CourseCreate, CourseResponse
from app.schemas.student import StudentResponse
from app.schemas.enrollment import EnrollmentCreate, EnrollmentResponse
from app.api.deps import get_current_user, get_current_instructor

router = APIRouter()


@router.get("/", response_model=List[CourseResponse], summary="List all Python modules")
def list_courses(
    skip: int = 0,
    limit: int = 100,
    db: Session = Depends(get_db),
    current_user: Student = Depends(get_current_user),
) -> Any:
    return db.query(Course).offset(skip).limit(limit).all()


@router.post("/", response_model=CourseResponse, status_code=status.HTTP_201_CREATED, summary="Create a new module")
def create_course(
    course_in: CourseCreate,
    db: Session = Depends(get_db),
    current_user: Student = Depends(get_current_instructor),
) -> Any:
    if db.query(Course).filter(Course.code == course_in.code).first():
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=f"Module with code '{course_in.code}' already exists."
        )
    course = Course(**course_in.model_dump())
    db.add(course)
    db.commit()
    db.refresh(course)
    return course


@router.get("/{course_id}", response_model=CourseResponse, summary="Get module details")
def get_course(
    course_id: int,
    db: Session = Depends(get_db),
    current_user: Student = Depends(get_current_user),
) -> Any:
    course = db.query(Course).filter(Course.id == course_id).first()
    if not course:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Module not found")
    return course


@router.post("/{course_id}/enroll", response_model=EnrollmentResponse, summary="Enroll student in module")
def enroll_student(
    course_id: int,
    enrollment_in: EnrollmentCreate,
    db: Session = Depends(get_db),
    current_user: Student = Depends(get_current_user),
) -> Any:
    course = db.query(Course).filter(Course.id == course_id).first()
    if not course:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Module not found")

    # Students can only enroll themselves; instructors/admins can enroll any student
    if current_user.role == "student" and enrollment_in.student_id != current_user.id:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Nu poți înscrie alți elevi."
        )

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
            detail="Student is already enrolled in this module."
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
    db: Session = Depends(get_db),
    current_user: Student = Depends(get_current_instructor),
) -> Any:
    enrollments = db.query(Enrollment).filter(
        Enrollment.course_id == course_id,
        Enrollment.status == "active"
    ).all()
    student_ids = [e.student_id for e in enrollments]
    if not student_ids:
        return []
    return db.query(Student).filter(Student.id.in_(student_ids)).all()

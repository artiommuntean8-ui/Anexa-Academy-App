from typing import List, Any
from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session

from app.db.session import get_db
from app.core.security import get_password_hash
from app.models.student import Student
from app.models.course import Course
from app.models.enrollment import Enrollment
from app.models.assignment import Assignment
from app.models.grade import Grade
from app.schemas.student import StudentCreate, StudentUpdate, StudentResponse
from app.schemas.dashboard import DashboardOverviewResponse

router = APIRouter()


@router.get("/", response_model=List[StudentResponse], summary="List all students")
def list_students(
    skip: int = 0,
    limit: int = 100,
    db: Session = Depends(get_db)
) -> Any:
    """Retrieve students list with pagination."""
    return db.query(Student).offset(skip).limit(limit).all()


@router.post("/", response_model=StudentResponse, status_code=status.HTTP_201_CREATED, summary="Create student")
def create_student(
    student_in: StudentCreate,
    db: Session = Depends(get_db)
) -> Any:
    """Create a new student profile."""
    if db.query(Student).filter(Student.student_code == student_in.student_code).first():
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=f"Student with code '{student_in.student_code}' already exists."
        )
    if db.query(Student).filter(Student.email == student_in.email).first():
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=f"Student with email '{student_in.email}' already exists."
        )

    student_data = student_in.model_dump()
    raw_password = student_data.pop("password")
    student_data["hashed_password"] = get_password_hash(raw_password)

    student = Student(**student_data)
    db.add(student)
    db.commit()
    db.refresh(student)
    return student


@router.get("/{student_id}/dashboard", response_model=DashboardOverviewResponse, summary="Student Dashboard Overview")
def get_student_dashboard(
    student_id: int,
    db: Session = Depends(get_db)
) -> Any:
    """
    Consolidated endpoint returning all essential KPIs and statistics for the desktop dashboard:
    - Student Profile
    - Total enrolled courses & credits
    - Calculated GPA / Average grade
    - List of enrolled courses
    - Upcoming assignments
    - Recent grades
    """
    student = db.query(Student).filter(Student.id == student_id).first()
    if not student:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Student not found")

    # Enrolled courses
    enrollments = db.query(Enrollment).filter(
        Enrollment.student_id == student_id,
        Enrollment.status == "active"
    ).all()
    course_ids = [e.course_id for e in enrollments]

    courses = db.query(Course).filter(Course.id.in_(course_ids)).all() if course_ids else []
    total_credits = sum(c.credits for c in courses)

    # Grades & GPA calculation
    grades = db.query(Grade).filter(Grade.student_id == student_id).all()
    if grades:
        average_grade = round(sum(g.score for g in grades) / len(grades), 2)
    else:
        average_grade = 0.0

    # Upcoming / Active assignments for enrolled courses
    assignments = db.query(Assignment).filter(Assignment.course_id.in_(course_ids)).all() if course_ids else []

    # Recent 5 grades
    recent_grades = db.query(Grade).filter(
        Grade.student_id == student_id
    ).order_by(Grade.graded_at.desc()).limit(5).all()

    return {
        "student": student,
        "total_enrolled_courses": len(courses),
        "total_credits": total_credits,
        "average_grade": average_grade,
        "enrolled_courses": courses,
        "upcoming_assignments": assignments,
        "recent_grades": recent_grades,
    }


@router.get("/{student_id}", response_model=StudentResponse, summary="Get student by ID")
def get_student(
    student_id: int,
    db: Session = Depends(get_db)
) -> Any:
    """Get single student details by ID."""
    student = db.query(Student).filter(Student.id == student_id).first()
    if not student:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Student not found")
    return student


@router.put("/{student_id}", response_model=StudentResponse, summary="Update student")
def update_student(
    student_id: int,
    student_in: StudentUpdate,
    db: Session = Depends(get_db)
) -> Any:
    """Update student fields."""
    student = db.query(Student).filter(Student.id == student_id).first()
    if not student:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Student not found")

    update_data = student_in.model_dump(exclude_unset=True)
    if "password" in update_data and update_data["password"]:
        raw_pwd = update_data.pop("password")
        student.hashed_password = get_password_hash(raw_pwd)

    for field, value in update_data.items():
        setattr(student, field, value)

    db.commit()
    db.refresh(student)
    return student


@router.delete("/{student_id}", status_code=status.HTTP_204_NO_CONTENT, summary="Delete student")
def delete_student(
    student_id: int,
    db: Session = Depends(get_db)
) -> None:
    """Delete student record."""
    student = db.query(Student).filter(Student.id == student_id).first()
    if not student:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Student not found")
    db.delete(student)
    db.commit()

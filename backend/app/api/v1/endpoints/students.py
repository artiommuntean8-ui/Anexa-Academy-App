from typing import List, Any
from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session

from app.db.session import get_db
from app.core.security import get_password_hash
from app.models.student import Student
from app.models.course import Course
from app.models.enrollment import Enrollment
from app.schemas.student import StudentCreate, StudentUpdate, StudentResponse
from app.schemas.dashboard import DashboardOverviewResponse
from app.schemas.progress import StudentProgressResponse, StudentProgressSummary
from app.services.progress import build_student_progress
from app.api.deps import get_current_user, get_current_instructor

router = APIRouter()


def _ensure_student_access(current_user: Student, student_id: int) -> None:
    if current_user.role == "student" and current_user.id != student_id:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Nu poți accesa datele altui elev.",
        )


@router.get("/", response_model=List[StudentResponse], summary="List all students")
def list_students(
    skip: int = 0,
    limit: int = 100,
    db: Session = Depends(get_db),
    current_user: Student = Depends(get_current_instructor),
) -> Any:
    return db.query(Student).filter(Student.role == "student").offset(skip).limit(limit).all()


@router.get("/progress/all", response_model=List[StudentProgressSummary], summary="All students progress")
def list_students_progress(
    db: Session = Depends(get_db),
    current_user: Student = Depends(get_current_instructor),
) -> Any:
    students = db.query(Student).filter(Student.role == "student", Student.is_active.is_(True)).all()
    summaries = []
    for student in students:
        progress = build_student_progress(db, student)
        summaries.append({
            "student_id": student.id,
            "student_code": student.student_code,
            "full_name": student.full_name,
            "overall_progress_percent": progress["overall_progress_percent"],
            "completed_lessons": progress["completed_lessons"],
            "total_lessons": progress["total_lessons"],
        })
    return summaries


@router.post("/", response_model=StudentResponse, status_code=status.HTTP_201_CREATED, summary="Create student")
def create_student(
    student_in: StudentCreate,
    db: Session = Depends(get_db),
    current_user: Student = Depends(get_current_instructor),
) -> Any:
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

    modules = db.query(Course).all()
    for module in modules:
        db.add(Enrollment(student_id=student.id, course_id=module.id, status="active"))
    db.commit()
    return student


@router.get("/me/progress", response_model=StudentProgressResponse, summary="Current user progress")
def get_my_progress(
    db: Session = Depends(get_db),
    current_user: Student = Depends(get_current_user),
) -> Any:
    if current_user.role != "student":
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Doar elevii pot accesa progresul personal.",
        )
    return build_student_progress(db, current_user, include_lessons=True)


@router.get("/{student_id}/progress", response_model=StudentProgressResponse, summary="Student progress")
def get_student_progress(
    student_id: int,
    db: Session = Depends(get_db),
    current_user: Student = Depends(get_current_user),
) -> Any:
    _ensure_student_access(current_user, student_id)
    student = db.query(Student).filter(Student.id == student_id).first()
    if not student:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Student not found")
    include_lessons = current_user.role in ["instructor", "admin"]
    return build_student_progress(db, student, include_lessons=include_lessons)


@router.get("/{student_id}/dashboard", response_model=DashboardOverviewResponse, summary="Student Dashboard Overview")
def get_student_dashboard(
    student_id: int,
    db: Session = Depends(get_db),
    current_user: Student = Depends(get_current_user),
) -> Any:
    _ensure_student_access(current_user, student_id)
    student = db.query(Student).filter(Student.id == student_id).first()
    if not student:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Student not found")

    from app.models.assignment import Assignment
    from app.models.grade import Grade

    progress = build_student_progress(db, student)
    enrollments = db.query(Enrollment).filter(
        Enrollment.student_id == student_id,
        Enrollment.status == "active",
    ).all()
    course_ids = [e.course_id for e in enrollments]
    courses = db.query(Course).filter(Course.id.in_(course_ids)).all() if course_ids else []
    assignments = db.query(Assignment).filter(Assignment.course_id.in_(course_ids)).all() if course_ids else []
    recent_grades = db.query(Grade).filter(
        Grade.student_id == student_id
    ).order_by(Grade.graded_at.desc()).limit(5).all()

    # Total credits = sum of credits from enrolled courses
    total_credits = sum(c.credits or 0 for c in courses)

    # Average grade = mean of all grades (0 if none)
    all_grades = db.query(Grade).filter(Grade.student_id == student_id).all()
    average_grade = round(sum(g.score for g in all_grades) / len(all_grades), 1) if all_grades else 0.0

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
    db: Session = Depends(get_db),
    current_user: Student = Depends(get_current_user),
) -> Any:
    _ensure_student_access(current_user, student_id)
    student = db.query(Student).filter(Student.id == student_id).first()
    if not student:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Student not found")
    return student


@router.put("/{student_id}", response_model=StudentResponse, summary="Update student")
def update_student(
    student_id: int,
    student_in: StudentUpdate,
    db: Session = Depends(get_db),
    current_user: Student = Depends(get_current_user),
) -> Any:
    _ensure_student_access(current_user, student_id)
    student = db.query(Student).filter(Student.id == student_id).first()
    if not student:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Student not found")

    update_data = student_in.model_dump(exclude_unset=True)

    # Security: students cannot change their own role, is_active, or student_code
    if current_user.role == "student":
        for forbidden_field in ("role", "is_active", "student_code"):
            update_data.pop(forbidden_field, None)

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
    db: Session = Depends(get_db),
    current_user: Student = Depends(get_current_instructor),
) -> None:
    student = db.query(Student).filter(Student.id == student_id).first()
    if not student:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Student not found")
    db.delete(student)
    db.commit()

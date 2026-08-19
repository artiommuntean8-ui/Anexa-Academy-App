from sqlalchemy.orm import Session

from app.models.student import Student
from app.models.course import Course
from app.models.assignment import Assignment
from app.models.enrollment import Enrollment
from app.models.grade import Grade


def _get_student_lessons(db: Session, student_id: int) -> tuple[list[Course], list[Assignment], dict[int, Grade]]:
    enrollments = db.query(Enrollment).filter(
        Enrollment.student_id == student_id,
        Enrollment.status == "active",
    ).all()
    module_ids = [e.course_id for e in enrollments]

    modules = (
        db.query(Course).filter(Course.id.in_(module_ids)).order_by(Course.id).all()
        if module_ids
        else []
    )
    lessons = (
        db.query(Assignment).filter(Assignment.course_id.in_(module_ids)).order_by(Assignment.id).all()
        if module_ids
        else []
    )

    grades = db.query(Grade).filter(Grade.student_id == student_id).all()
    grade_map = {g.assignment_id: g for g in grades}
    return modules, lessons, grade_map


def build_student_progress(db: Session, student: Student, include_lessons: bool = False) -> dict:
    modules, lessons, grade_map = _get_student_lessons(db, student.id)
    module_map = {m.id: m for m in modules}

    total_lessons = len(lessons)
    completed_lessons = sum(1 for lesson in lessons if lesson.id in grade_map)

    overall_percent = round((completed_lessons / total_lessons) * 100, 1) if total_lessons else 0.0

    module_progress = []
    for module in modules:
        module_lessons = [lesson for lesson in lessons if lesson.course_id == module.id]
        module_completed = sum(1 for lesson in module_lessons if lesson.id in grade_map)
        module_total = len(module_lessons)
        module_percent = round((module_completed / module_total) * 100, 1) if module_total else 0.0
        module_progress.append({
            "module_id": module.id,
            "module_code": module.code,
            "module_title": module.title,
            "total_lessons": module_total,
            "completed_lessons": module_completed,
            "progress_percent": module_percent,
        })

    result = {
        "student": student,
        "overall_progress_percent": overall_percent,
        "total_lessons": total_lessons,
        "completed_lessons": completed_lessons,
        "modules": module_progress,
    }

    if include_lessons:
        lesson_statuses = []
        for lesson in lessons:
            grade = grade_map.get(lesson.id)
            module = module_map.get(lesson.course_id)
            lesson_statuses.append({
                "lesson_id": lesson.id,
                "lesson_title": lesson.title,
                "module_id": lesson.course_id,
                "module_title": module.title if module else "",
                "is_completed": grade is not None,
                "completed_at": grade.graded_at.isoformat() if grade else None,
                "feedback": grade.feedback if grade else None,
            })
        result["lessons"] = lesson_statuses

    return result

import os
import sys

sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), "backend")))

import app.models  # noqa: F401 — register all ORM tables
from app.db.session import engine, SessionLocal, Base
from app.core.security import get_password_hash
from app.models.student import Student
from app.models.course import Course
from app.models.assignment import Assignment
from app.models.test_case import TestCase
from app.models.enrollment import Enrollment
from app.models.gamification import Badge as BadgeModel


def seed_demo_data(db):
    """Seed demo data for the application."""
    # Create default badges
    badges_data = [
        {"code": "FIRST_BLOOD", "title": "First Blood", "description": "Prima soluție corectă", "icon_name": "first_blood", "xp_reward": 25},
        {"code": "PERFECT_ATTEMPT", "title": "Perfect Attempt", "description": "Soluție corectă din prima încercare", "icon_name": "perfect", "xp_reward": 15},
        {"code": "SPEED_DEMON", "title": "Speed Demon", "description": "Soluție rapidă (<300ms)", "icon_name": "speed", "xp_reward": 20},
        {"code": "STREAK_3", "title": "3-Day Streak", "description": "3 zile consecutive de activitate", "icon_name": "streak", "xp_reward": 30},
        {"code": "PYTHON_PRO", "title": "Python Pro", "description": "300+ XP acumulate", "icon_name": "pro", "xp_reward": 50},
    ]

    for badge_data in badges_data:
        existing = db.query(BadgeModel).filter(BadgeModel.code == badge_data["code"]).first()
        if not existing:
            db.add(BadgeModel(**badge_data))

    # Create demo users
    users = [
        Student(
            student_code="PROF001",
            full_name="Mihail Potlog",
            email="profesor@anexa.md",
            hashed_password=get_password_hash("profesor123"),
            department="Inginerie Software",
            semester=1,
            role="instructor",
            is_active=True
        ),
        Student(
            student_code="STU001",
            full_name="Artiom Muntean",
            email="artiom@anexa.md",
            hashed_password=get_password_hash("student123"),
            department="Inginerie Software",
            semester=1,
            role="student",
            is_active=True
        ),
        Student(
            student_code="STU002",
            full_name="Elev Test",
            email="elev@anexa.md",
            hashed_password=get_password_hash("student123"),
            department="Inginerie Software",
            semester=1,
            role="student",
            is_active=True
        ),
    ]

    for user in users:
        existing = db.query(Student).filter(Student.email == user.email).first()
        if not existing:
            db.add(user)

    db.commit()


def _ensure_anexa_lab_course(db) -> Course:
    course = db.query(Course).filter(Course.code == "ANX-LAB").first()
    if not course:
        course = Course(
            code="ANX-LAB",
            title="Laborator Anexa Academy",
            description="Exerciții interactive evaluate în Sandbox Docker.",
            instructor_name="Mihail Potlog",
            semester=1,
            credits=5,
        )
        db.add(course)
        db.commit()
        db.refresh(course)
    return course


def _ensure_lab_assignments(db, course: Course) -> None:
    assignments = [
        ("Print Salut", "Afișează mesajul: 'Salut, Anexa Academy!'", "print('Salut, Anexa Academy!')"),
        ("Suma a două numere", "Citește două numere și afișează suma.", "a = int(input())\nb = int(input())\nprint(a+b)"),
        ("Par sau Impar", "Afișează 'Par' sau 'Impar'.", "n = int(input())\nprint('Par' if n % 2 == 0 else 'Impar')"),
        ("Inversare Text", "Inversează textul dat.", "t = input()\nprint(t[::-1])"),
        ("Calcul Factorial", "Calculează factorialul unui număr.", "import math\nn = int(input())\nprint(math.factorial(n))"),
    ]
    test_cases_data = [
        [("n/a", "Salut, Anexa Academy!", False)],
        [("3\n5", "8", False), ("-2\n10", "8", True), ("0\n0", "0", True)],
        [("4", "Par", False), ("7", "Impar", False), ("0", "Par", True)],
        [("python", "nohtyp", False), ("Anexa", "axenA", True)],
        [("5", "120", False), ("3", "6", True)],
    ]

    for i, (title, desc, code) in enumerate(assignments):
        assign = db.query(Assignment).filter(
            Assignment.course_id == course.id,
            Assignment.title == title,
        ).first()
        if not assign:
            assign = Assignment(
                title=title,
                description=desc,
                starter_code=code,
                course_id=course.id,
            )
            db.add(assign)
            db.commit()
            db.refresh(assign)

        existing = db.query(TestCase).filter(TestCase.assignment_id == assign.id).count()
        if existing == 0:
            for tc in test_cases_data[i]:
                db.add(
                    TestCase(
                        assignment_id=assign.id,
                        input_data=tc[0],
                        expected_output=tc[1],
                        is_hidden=tc[2],
                    )
                )
    db.commit()


def seed_db():
    print("Curatare si populare baza de date SQLite...")
    Base.metadata.drop_all(bind=engine)
    Base.metadata.create_all(bind=engine)

    db = SessionLocal()
    try:
        seed_demo_data(db)
        course = _ensure_anexa_lab_course(db)
        _ensure_lab_assignments(db, course)

        students = db.query(Student).filter(Student.role == "student").all()
        for student in students:
            existing = db.query(Enrollment).filter(
                Enrollment.student_id == student.id,
                Enrollment.course_id == course.id,
            ).first()
            if not existing:
                db.add(Enrollment(student_id=student.id, course_id=course.id, status="active"))
        db.commit()

        print("[SUCCESS] Baza de date a fost populata cu succes!")
        print("Credentiale:")
        print("Instructor: profesor@anexa.md / profesor123")
        print("Elev: artiom@anexa.md / student123")
        print("Elev: elev@anexa.md / student123")
    except Exception as e:
        print(f"[ERROR] {e}")
        db.rollback()
        raise
    finally:
        db.close()


def init_db():
    """Initialize database schema without dropping data."""
    Base.metadata.create_all(bind=engine)


if __name__ == "__main__":
    seed_db()

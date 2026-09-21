import os
import sys

sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), "backend")))

import app.models  # noqa: F401 — register all ORM tables
from app.db.session import engine, SessionLocal, Base
from app.db.init_db import seed_demo_data
from app.core.security import get_password_hash
from app.models.student import Student
from app.models.course import Course
from app.models.assignment import Assignment
from app.models.test_case import TestCase
from app.models.enrollment import Enrollment


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

        # Guarantee documented credentials (hash refresh)
        for email, password in (
            ("profesor@anexa.md", "profesor123"),
            ("artiom@anexa.md", "student123"),
            ("elev@anexa.md", "student123"),
        ):
            user = db.query(Student).filter(Student.email == email).first()
            if user:
                user.hashed_password = get_password_hash(password)
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


if __name__ == "__main__":
    seed_db()

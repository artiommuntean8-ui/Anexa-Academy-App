import json
import datetime
import sqlite3
from sqlalchemy import text
from sqlalchemy.orm import Session
from app.db.session import engine, Base
from app.core.security import get_password_hash
import app.models  # noqa: F401
from app.models.student import Student
from app.models.course import Course
from app.models.enrollment import Enrollment
from app.models.assignment import Assignment
from app.models.grade import Grade
from app.models.achievement import Achievement, StudentAchievement


INITIAL_ACHIEVEMENTS = [
    {
        "code": "FIRST_CODE",
        "title": "Primul Pas în Python",
        "description": "Rulează și validează primul tău cod cu succes în consolă.",
        "icon": "🚀",
        "xp_reward": 50,
        "category": "general"
    },
    {
        "code": "PERFECT_SCORE",
        "title": "Perfecțiune Academică",
        "description": "Obține un punctaj impecabil de 100 puncte la un exercițiu.",
        "icon": "⭐",
        "xp_reward": 100,
        "category": "mastery"
    },
    {
        "code": "LOOP_MASTER",
        "title": "Maestru al Buclelor",
        "description": "Rezolvă un exercițiu ce conține instrucțiuni for sau while.",
        "icon": "⚡",
        "xp_reward": 150,
        "category": "python"
    },
    {
        "code": "FUNCTION_PRO",
        "title": "Arhitect de Funcții",
        "description": "Scrie și validează o funcție modulară cu parametri și return.",
        "icon": "🧠",
        "xp_reward": 150,
        "category": "python"
    },
    {
        "code": "TRIPLE_CROWN",
        "title": "Tridentul Cunoașterii",
        "description": "Finalizează cu succes cel puțin 3 teme notate.",
        "icon": "🏆",
        "xp_reward": 200,
        "category": "mastery"
    },
    {
        "code": "DATA_WIZARD",
        "title": "Vrăjitorul Structurilor",
        "description": "Manipulează cu succes colecții de date (liste sau dicționare).",
        "icon": "🔮",
        "xp_reward": 150,
        "category": "python"
    },
]

PYTHON_MODULES = [
    {
        "code": "PY-01",
        "title": "Primii pași în Python",
        "description": "Înveți ce este Python, cum rulezi cod și cum afișezi mesaje în consolă.",
        "instructor_name": "Prof. Ana Ionescu",
        "lessons": [
            {
                "title": "Comanda print() și afișarea",
                "description": "Scrie o instrucțiune print care afișează 'Salut, ArkiTech!' în consolă.",
                "starter_code": "print('Salut, ArkiTech!')\n",
                "test_cases": json.dumps([
                    {"type": "stdout_contains", "expected": "Salut", "description": "Verifică dacă mesajul conține 'Salut'"},
                    {"type": "stdout_contains", "expected": "ArkiTech", "description": "Verifică dacă mesajul conține 'ArkiTech'"}
                ])
            },
            {
                "title": "Variabile și tipuri de date",
                "description": "Definește două variabile x=10 și y=20 și afișează suma lor.",
                "starter_code": "x = 10\ny = 20\nprint(x + y)\n",
                "test_cases": json.dumps([
                    {"type": "stdout_contains", "expected": "30", "description": "Verifică dacă suma afișată este 30"}
                ])
            }
        ],
    },
    {
        "code": "PY-02",
        "title": "Decizii în cod (if / else)",
        "description": "Înveți să faci programul să aleagă ramura potrivită cu if și else.",
        "instructor_name": "Prof. Ana Ionescu",
        "lessons": [
            {
                "title": "Verificare Par / Impar",
                "description": "Creează o funcție este_par(numar) care returnează True dacă numărul este par și False dacă este impar.",
                "starter_code": "def este_par(numar):\n    return numar % 2 == 0\n",
                "test_cases": json.dumps([
                    {"type": "call", "call": "este_par(4)", "expected": True, "description": "Test 4 este par"},
                    {"type": "call", "call": "este_par(7)", "expected": False, "description": "Test 7 este impar"},
                    {"type": "call", "call": "este_par(0)", "expected": True, "description": "Test 0 este par"}
                ])
            }
        ],
    },
    {
        "code": "PY-03",
        "title": "Repetări (bucle for & while)",
        "description": "Înveți cum repetă un program anumite acțiuni automat cu bucle.",
        "instructor_name": "Prof. Ana Ionescu",
        "lessons": [
            {
                "title": "Suma primelor N numere",
                "description": "Creează o funcție suma_pana_la(n) care calculează suma 1 + 2 + ... + n folosind o buclă.",
                "starter_code": "def suma_pana_la(n):\n    total = 0\n    for i in range(1, n + 1):\n        total += i\n    return total\n",
                "test_cases": json.dumps([
                    {"type": "call", "call": "suma_pana_la(5)", "expected": 15, "description": "Suma până la 5 (1+2+3+4+5=15)"},
                    {"type": "call", "call": "suma_pana_la(10)", "expected": 55, "description": "Suma până la 10 (55)"}
                ])
            }
        ],
    },
    {
        "code": "PY-04",
        "title": "Funcții & Modularitate",
        "description": "Înveți să îți organizezi codul în funcții reutilizabile și flexibile.",
        "instructor_name": "Prof. Ana Ionescu",
        "lessons": [
            {
                "title": "Mini-Calculator de operații",
                "description": "Creează funcția calculator(a, b, op) care suportă '+', '-', '*'.",
                "starter_code": "def calculator(a, b, op):\n    if op == '+': return a + b\n    elif op == '-': return a - b\n    elif op == '*': return a * b\n    return 0\n",
                "test_cases": json.dumps([
                    {"type": "call", "call": "calculator(10, 5, '+')", "expected": 15, "description": "10 + 5 = 15"},
                    {"type": "call", "call": "calculator(20, 8, '-')", "expected": 12, "description": "20 - 8 = 12"},
                    {"type": "call", "call": "calculator(6, 7, '*')", "expected": 42, "description": "6 * 7 = 42"}
                ])
            }
        ],
    }
]

DEMO_USERS = [
    {
        "student_code": "ARK-2026-001",
        "full_name": "Artiom Muntean",
        "email": "artiom.muntean@arkitech.academy",
        "password": "ArkiTech2026!",
        "role": "student",
        "department": "Software Architecture & Engineering",
        "semester": 2,
    },
    {
        "student_code": "TEACH-001",
        "full_name": "Prof. Ana Ionescu",
        "email": "prof.an@pythonkids.ro",
        "password": "Prof2026!",
        "role": "instructor",
        "department": "Academia ArkiTech",
        "semester": 1,
    },
    {
        "student_code": "ELEV-001",
        "full_name": "Andrei Popescu",
        "email": "andrei@pythonkids.ro",
        "password": "Elev2026!",
        "role": "student",
        "department": "Grupa A (Python Junior)",
        "semester": 1,
    },
    {
        "student_code": "ELEV-002",
        "full_name": "Maria Dumitrescu",
        "email": "maria@pythonkids.ro",
        "password": "Elev2026!",
        "role": "student",
        "department": "Grupa A (Python Junior)",
        "semester": 1,
    },
    {
        "student_code": "ELEV-003",
        "full_name": "David Munteanu",
        "email": "david@pythonkids.ro",
        "password": "Elev2026!",
        "role": "student",
        "department": "Grupa B (Python Junior)",
        "semester": 1,
    },
]


def init_db() -> None:
    Base.metadata.create_all(bind=engine)
    
    # Auto-migration: check if starter_code or test_cases are missing in assignments
    with engine.connect() as conn:
        try:
            res = conn.execute(text("PRAGMA table_info(assignments);")).fetchall()
            col_names = [r[1] for r in res]
            if "starter_code" not in col_names:
                conn.execute(text("ALTER TABLE assignments ADD COLUMN starter_code TEXT;"))
            if "test_cases" not in col_names:
                conn.execute(text("ALTER TABLE assignments ADD COLUMN test_cases TEXT;"))
            conn.commit()
        except Exception as e:
            print(f"Migration check: {e}")


def _ensure_user(db: Session, user_data: dict) -> Student:
    student = db.query(Student).filter(Student.email == user_data["email"]).first()
    password_hash = get_password_hash(user_data["password"])
    if not student:
        student = Student(
            student_code=user_data["student_code"],
            full_name=user_data["full_name"],
            email=user_data["email"],
            hashed_password=password_hash,
            role=user_data["role"],
            department=user_data["department"],
            semester=user_data["semester"],
            is_active=True,
        )
        db.add(student)
        db.commit()
        db.refresh(student)
    else:
        student.hashed_password = password_hash
        student.full_name = user_data["full_name"]
        student.role = user_data["role"]
        student.department = user_data["department"]
        student.student_code = user_data["student_code"]
        student.is_active = True
        db.commit()
    return student


def _ensure_achievements(db: Session) -> None:
    for ach_data in INITIAL_ACHIEVEMENTS:
        existing = db.query(Achievement).filter(Achievement.code == ach_data["code"]).first()
        if not existing:
            db.add(Achievement(
                code=ach_data["code"],
                title=ach_data["title"],
                description=ach_data["description"],
                icon=ach_data["icon"],
                xp_reward=ach_data["xp_reward"],
                category=ach_data["category"],
            ))
        else:
            existing.title = ach_data["title"]
            existing.description = ach_data["description"]
            existing.icon = ach_data["icon"]
            existing.xp_reward = ach_data["xp_reward"]
    db.commit()


def _ensure_module(db: Session, module_data: dict) -> Course:
    module = db.query(Course).filter(Course.code == module_data["code"]).first()
    if not module:
        module = Course(
            code=module_data["code"],
            title=module_data["title"],
            description=module_data["description"],
            instructor_name=module_data["instructor_name"],
            semester=1,
            credits=len(module_data["lessons"]) * 2,
        )
        db.add(module)
        db.commit()
        db.refresh(module)
    else:
        module.title = module_data["title"]
        module.description = module_data["description"]
        module.instructor_name = module_data["instructor_name"]
        module.credits = len(module_data["lessons"]) * 2
        db.commit()

    for lesson_item in module_data["lessons"]:
        existing = db.query(Assignment).filter(
            Assignment.course_id == module.id,
            Assignment.title == lesson_item["title"],
        ).first()
        if not existing:
            db.add(Assignment(
                course_id=module.id,
                title=lesson_item["title"],
                description=lesson_item["description"],
                starter_code=lesson_item.get("starter_code", ""),
                test_cases=lesson_item.get("test_cases", "[]"),
                max_score=100.0,
                due_date=datetime.datetime.utcnow() + datetime.timedelta(days=7),
            ))
        else:
            existing.description = lesson_item["description"]
            existing.starter_code = lesson_item.get("starter_code", "")
            existing.test_cases = lesson_item.get("test_cases", "[]")
    db.commit()
    return module


def _enroll_student_in_all_modules(db: Session, student: Student) -> None:
    modules = db.query(Course).all()
    for module in modules:
        existing = db.query(Enrollment).filter(
            Enrollment.student_id == student.id,
            Enrollment.course_id == module.id,
        ).first()
        if not existing:
            db.add(Enrollment(
                student_id=student.id,
                course_id=module.id,
                status="active",
            ))
    db.commit()


def seed_demo_data(db: Session) -> None:
    """Seed initial achievements, curriculum, users, enrollments and sample progress."""
    _ensure_achievements(db)

    for user_data in DEMO_USERS:
        _ensure_user(db, user_data)

    for module_data in PYTHON_MODULES:
        _ensure_module(db, module_data)

    students = db.query(Student).filter(Student.role == "student").all()
    for student in students:
        _enroll_student_in_all_modules(db, student)


if __name__ == "__main__":
    from app.db.session import SessionLocal
    print("Initialising database tables...")
    init_db()
    db = SessionLocal()
    try:
        print("Seeding demo data & achievements...")
        seed_demo_data(db)
        print("Done!")
    finally:
        db.close()

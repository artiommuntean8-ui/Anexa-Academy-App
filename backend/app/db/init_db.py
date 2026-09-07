import datetime
from sqlalchemy.orm import Session
from app.db.session import engine, Base
from app.core.security import get_password_hash
import app.models  # noqa: F401
from app.models.student import Student
from app.models.course import Course
from app.models.enrollment import Enrollment
from app.models.assignment import Assignment
from app.models.grade import Grade


PYTHON_MODULES = [
    {
        "code": "PY-01",
        "title": "Primii pași în Python",
        "description": "Înveți ce este Python, cum rulezi cod și cum afișezi mesaje.",
        "instructor_name": "Prof. Ana Ionescu",
        "lessons": [
            "Ce este Python?",
            "Comanda print()",
            "Variabile simple",
            "Numere și text",
        ],
    },
    {
        "code": "PY-02",
        "title": "Decizii în cod (if / else)",
        "description": "Înveți să faci programul să aleagă ramura potrivită cu if și else.",
        "instructor_name": "Prof. Ana Ionescu",
        "lessons": [
            "Operatori de comparare",
            "Instrucțiunea if",
            "Structura if / else",
        ],
    },
    {
        "code": "PY-03",
        "title": "Repetări (bucle for & while)",
        "description": "Înveți cum repetă un program anumite acțiuni automat.",
        "instructor_name": "Prof. Ana Ionescu",
        "lessons": [
            "Bucla for",
            "Funcția range()",
            "Bucla while",
            "Exercițiu: Ghicește numărul",
        ],
    },
    {
        "code": "PY-04",
        "title": "Funcții & Modularitate",
        "description": "Înveți să îți organizezi codul în funcții reutilizabile.",
        "instructor_name": "Prof. Ana Ionescu",
        "lessons": [
            "Ce este o funcție?",
            "Parametri și return",
            "Mini-proiect: Calculator",
        ],
    },
    {
        "code": "PY-05",
        "title": "Structuri de Date (Liste & Dicționare)",
        "description": "Înveți să stochezi colecții de valori într-o singură variabilă.",
        "instructor_name": "Prof. Ana Ionescu",
        "lessons": [
            "Liste și indexare",
            "Parcurgerea listelor",
            "Dicționare simple",
        ],
    },
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

    for lesson_title in module_data["lessons"]:
        existing = db.query(Assignment).filter(
            Assignment.course_id == module.id,
            Assignment.title == lesson_title,
        ).first()
        if not existing:
            db.add(Assignment(
                course_id=module.id,
                title=lesson_title,
                description=f"Lecție și exercițiu practic din modulul {module.title}",
                max_score=100.0,
                due_date=datetime.datetime.utcnow() + datetime.timedelta(days=7),
            ))
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


def _seed_demo_progress(db: Session) -> None:
    artiom = db.query(Student).filter(Student.email == "artiom.muntean@arkitech.academy").first()
    andrei = db.query(Student).filter(Student.email == "andrei@pythonkids.ro").first()
    maria = db.query(Student).filter(Student.email == "maria@pythonkids.ro").first()

    students_to_grade = [s for s in [artiom, andrei, maria] if s is not None]
    if not students_to_grade:
        return

    py01 = db.query(Course).filter(Course.code == "PY-01").first()
    py02 = db.query(Course).filter(Course.code == "PY-02").first()
    if not py01:
        return

    lessons = db.query(Assignment).filter(Assignment.course_id.in_([py01.id, py02.id] if py02 else [py01.id])).all()
    
    for st in students_to_grade:
        for i, lesson in enumerate(lessons[:3]):
            existing = db.query(Grade).filter(
                Grade.student_id == st.id,
                Grade.assignment_id == lesson.id,
            ).first()
            if not existing:
                db.add(Grade(
                    assignment_id=lesson.id,
                    student_id=st.id,
                    score=98.5 if st == artiom else 100.0,
                    feedback="Implementare excelentă a cerințelor și cod curat!",
                ))
    db.commit()


def seed_demo_data(db: Session) -> None:
    """Seed ArkiTech curriculum, users, enrollments and sample progress."""
    for user_data in DEMO_USERS:
        _ensure_user(db, user_data)

    for module_data in PYTHON_MODULES:
        _ensure_module(db, module_data)

    students = db.query(Student).filter(Student.role == "student").all()
    for student in students:
        _enroll_student_in_all_modules(db, student)

    _seed_demo_progress(db)


if __name__ == "__main__":
    from app.db.session import SessionLocal
    print("Initialising database tables...")
    init_db()
    db = SessionLocal()
    try:
        print("Seeding demo data...")
        seed_demo_data(db)
        print("Done!")
    finally:
        db.close()

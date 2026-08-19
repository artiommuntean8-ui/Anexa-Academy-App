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
        "instructor_name": "Prof. Ana",
        "lessons": [
            "Ce este Python?",
            "Comanda print()",
            "Variabile simple",
            "Numere și text",
        ],
    },
    {
        "code": "PY-02",
        "title": "Decizii în cod",
        "description": "Înveți să faci programul să aleagă cu if și else.",
        "instructor_name": "Prof. Ana",
        "lessons": [
            "Operatori de comparare",
            "Instrucțiunea if",
            "if / else",
        ],
    },
    {
        "code": "PY-03",
        "title": "Repetări (bucle)",
        "description": "Înveți cum repetă un program anumite acțiuni cu for și while.",
        "instructor_name": "Prof. Ana",
        "lessons": [
            "Bucla for",
            "Funcția range()",
            "Bucla while",
            "Exercițiu: ghicește numărul",
        ],
    },
    {
        "code": "PY-04",
        "title": "Funcții",
        "description": "Înveți să îți organizezi codul în funcții reutilizabile.",
        "instructor_name": "Prof. Ana",
        "lessons": [
            "Ce este o funcție?",
            "Parametri și return",
            "Mini-proiect: calculator",
        ],
    },
    {
        "code": "PY-05",
        "title": "Liste și dicționare",
        "description": "Înveți să stochezi mai multe valori într-o singură variabilă.",
        "instructor_name": "Prof. Ana",
        "lessons": [
            "Liste",
            "Parcurgerea listelor",
            "Dicționare simple",
        ],
    },
]

DEMO_USERS = [
    {
        "student_code": "TEACH-001",
        "full_name": "Prof. Ana Ionescu",
        "email": "prof.an@pythonkids.ro",
        "password": "Prof2026!",
        "role": "instructor",
        "department": "Python pentru copii",
        "semester": 1,
    },
    {
        "student_code": "ELEV-001",
        "full_name": "Andrei Popescu",
        "email": "andrei@pythonkids.ro",
        "password": "Elev2026!",
        "role": "student",
        "department": "Grupa A (10-12 ani)",
        "semester": 1,
    },
    {
        "student_code": "ELEV-002",
        "full_name": "Maria Dumitrescu",
        "email": "maria@pythonkids.ro",
        "password": "Elev2026!",
        "role": "student",
        "department": "Grupa A (10-12 ani)",
        "semester": 1,
    },
    {
        "student_code": "ELEV-003",
        "full_name": "David Munteanu",
        "email": "david@pythonkids.ro",
        "password": "Elev2026!",
        "role": "student",
        "department": "Grupa B (10-12 ani)",
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
            credits=len(module_data["lessons"]),
        )
        db.add(module)
        db.commit()
        db.refresh(module)
    else:
        module.title = module_data["title"]
        module.description = module_data["description"]
        module.instructor_name = module_data["instructor_name"]
        module.credits = len(module_data["lessons"])
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
                description=f"Lecție din modulul {module.title}",
                max_score=100.0,
                due_date=None,
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
    andrei = db.query(Student).filter(Student.email == "andrei@pythonkids.ro").first()
    maria = db.query(Student).filter(Student.email == "maria@pythonkids.ro").first()
    if not andrei or not maria:
        return

    py01 = db.query(Course).filter(Course.code == "PY-01").first()
    py02 = db.query(Course).filter(Course.code == "PY-02").first()
    if not py01 or not py02:
        return

    andrei_lessons = db.query(Assignment).filter(Assignment.course_id.in_([py01.id, py02.id])).all()
    for i, lesson in enumerate(andrei_lessons[:5]):
        existing = db.query(Grade).filter(
            Grade.student_id == andrei.id,
            Grade.assignment_id == lesson.id,
        ).first()
        if not existing:
            db.add(Grade(
                assignment_id=lesson.id,
                student_id=andrei.id,
                score=100.0,
                feedback="Foarte bine! Lecția este completă.",
            ))

    maria_lessons = db.query(Assignment).filter(Assignment.course_id == py01.id).all()
    for lesson in maria_lessons[:3]:
        existing = db.query(Grade).filter(
            Grade.student_id == maria.id,
            Grade.assignment_id == lesson.id,
        ).first()
        if not existing:
            db.add(Grade(
                assignment_id=lesson.id,
                student_id=maria.id,
                score=100.0,
                feedback="Bravo! Continuă așa!",
            ))
    db.commit()


def seed_demo_data(db: Session) -> None:
    """Seed Python Kids curriculum, users, enrollments and sample progress."""
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
        print("Seeding Python Kids demo data...")
        seed_demo_data(db)
        print("Done!")
    finally:
        db.close()

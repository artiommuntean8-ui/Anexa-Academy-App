import datetime
from sqlalchemy.orm import Session
from app.db.session import engine, Base
from app.core.security import get_password_hash
import app.models  # Ensure all models are loaded in SQLAlchemy metadata
from app.models.student import Student
from app.models.course import Course
from app.models.enrollment import Enrollment
from app.models.assignment import Assignment
from app.models.grade import Grade


def init_db() -> None:
    """Create database tables."""
    Base.metadata.create_all(bind=engine)


def seed_demo_data(db: Session) -> None:
    """Seed initial demo data for Academia ArkiTech."""
    # Check if student already exists
    student = db.query(Student).filter(Student.student_code == "ARK-2026-001").first()
    demo_password_hash = get_password_hash("ArkiTech2026!")

    if not student:
        student = Student(
            student_code="ARK-2026-001",
            full_name="Artiom Muntean",
            email="artiom.muntean@arkitech.academy",
            hashed_password=demo_password_hash,
            role="student",
            department="Software Architecture & Engineering",
            semester=2,
            is_active=True
        )
        db.add(student)
        db.commit()
        db.refresh(student)
    else:
        # Ensure password is set
        if not getattr(student, "hashed_password", None):
            student.hashed_password = demo_password_hash
            db.commit()

    # Check courses
    course1 = db.query(Course).filter(Course.code == "CS-401").first()
    if not course1:
        course1 = Course(
            code="CS-401",
            title="Arhitecturi Avansate de Backend cu FastAPI",
            description="Dezvoltarea sistemelor distribuite asincrone de înaltă performanță.",
            instructor_name="Prof. Dr. Alexandru Popescu",
            semester=2,
            credits=6
        )
        db.add(course1)

    course2 = db.query(Course).filter(Course.code == "CS-402").first()
    if not course2:
        course2 = Course(
            code="CS-402",
            title="Dezvoltare Aplicații Desktop GUI (Qt/PySide)",
            description="Proiectarea interfețelor grafice moderne pentru sisteme desktop.",
            instructor_name="Ing. Mihai Radu",
            semester=2,
            credits=5
        )
        db.add(course2)

    db.commit()
    if course1:
        db.refresh(course1)
    if course2:
        db.refresh(course2)

    # Enrollments
    for c in [course1, course2]:
        if c:
            existing_enrollment = db.query(Enrollment).filter(
                Enrollment.student_id == student.id,
                Enrollment.course_id == c.id
            ).first()
            if not existing_enrollment:
                enrollment = Enrollment(
                    student_id=student.id,
                    course_id=c.id,
                    status="active"
                )
                db.add(enrollment)

    db.commit()

    # Assignments & Grades
    if course1:
        assignment1 = db.query(Assignment).filter(Assignment.title == "Proiect 1: REST API & Asincronism").first()
        if not assignment1:
            assignment1 = Assignment(
                course_id=course1.id,
                title="Proiect 1: REST API & Asincronism",
                description="Construirea unui API REST complet documentat în Swagger.",
                max_score=100.0,
                due_date=datetime.datetime.utcnow() + datetime.timedelta(days=7)
            )
            db.add(assignment1)
            db.commit()
            db.refresh(assignment1)

            # Grade for student
            grade1 = Grade(
                assignment_id=assignment1.id,
                student_id=student.id,
                score=98.5,
                feedback="Implementare excelentă a arhitecturii și a middleware-ului CORS."
            )
            db.add(grade1)
            db.commit()


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

from sqlalchemy.orm import Session
from app.models.student import Student

def add_xp(db: Session, student_id: int, xp_amount: int):
    student = db.query(Student).filter(Student.id == student_id).first()
    if student:
        # Asigurăm inițializarea dacă coloanele lipsesc sau sunt None
        # Notă: Asigură-te că modelele SQLAlchemy au aceste coloane adăugate
        current_xp = getattr(student, 'xp', 0) or 0
        student.xp = current_xp + xp_amount
        student.level = (student.xp // 100) + 1
        db.commit()
    return student

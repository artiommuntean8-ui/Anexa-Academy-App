import datetime
from sqlalchemy import Column, Integer, Text, Float, DateTime, ForeignKey, UniqueConstraint
from sqlalchemy.orm import relationship

from app.db.session import Base


class Grade(Base):
    __tablename__ = "grades"

    id = Column(Integer, primary_key=True, index=True)
    assignment_id = Column(Integer, ForeignKey("assignments.id", ondelete="CASCADE"), nullable=False)
    student_id = Column(Integer, ForeignKey("students.id", ondelete="CASCADE"), nullable=False)
    score = Column(Float, nullable=False)
    feedback = Column(Text, nullable=True)
    graded_at = Column(DateTime, default=datetime.datetime.utcnow)

    # Relationships
    assignment = relationship("Assignment", back_populates="grades")
    student = relationship("Student", back_populates="grades")

    __table_args__ = (
        UniqueConstraint("assignment_id", "student_id", name="uq_assignment_student_grade"),
    )

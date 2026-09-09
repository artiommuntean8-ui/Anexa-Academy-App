import datetime
from sqlalchemy import Column, Integer, String, Text, Float, DateTime, ForeignKey
from sqlalchemy.orm import relationship
from app.db.session import Base


class Assignment(Base):
    __tablename__ = "assignments"

    id = Column(Integer, primary_key=True, index=True)
    test_cases_rel = relationship("TestCase", back_populates="assignment", cascade="all, delete-orphan")

    course_id = Column(Integer, ForeignKey("courses.id", ondelete="CASCADE"), nullable=False)
    title = Column(String(200), nullable=False)
    description = Column(Text, nullable=True)
    starter_code = Column(Text, nullable=True)
    old_test_cases_data = Column(Text, nullable=True)  # Redenumit pentru a evita conflictul
    max_score = Column(Float, default=100.0)
    due_date = Column(DateTime, nullable=True)
    created_at = Column(DateTime, default=datetime.datetime.utcnow)

    # Relationships
    course = relationship("Course", back_populates="assignments")
    grades = relationship("Grade", back_populates="assignment", cascade="all, delete-orphan")

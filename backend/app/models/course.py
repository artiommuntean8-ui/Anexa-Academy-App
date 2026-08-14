import datetime
from sqlalchemy import Column, Integer, String, Text, DateTime
from sqlalchemy.orm import relationship

from app.db.session import Base


class Course(Base):
    __tablename__ = "courses"

    id = Column(Integer, primary_key=True, index=True)
    code = Column(String(20), unique=True, index=True, nullable=False)
    title = Column(String(200), nullable=False, index=True)
    description = Column(Text, nullable=True)
    instructor_name = Column(String(150), nullable=False)
    semester = Column(Integer, default=1)
    credits = Column(Integer, default=5)
    created_at = Column(DateTime, default=datetime.datetime.utcnow)

    # Relationships
    enrollments = relationship("Enrollment", back_populates="course", cascade="all, delete-orphan")
    assignments = relationship("Assignment", back_populates="course", cascade="all, delete-orphan")

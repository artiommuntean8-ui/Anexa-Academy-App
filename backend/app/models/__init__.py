"""
SQLAlchemy models package.
Import all models here for Alembic and global metadata registration.
"""
from app.db.session import Base
from app.models.student import Student
from app.models.course import Course
from app.models.enrollment import Enrollment
from app.models.assignment import Assignment
from app.models.grade import Grade

__all__ = [
    "Base",
    "Student",
    "Course",
    "Enrollment",
    "Assignment",
    "Grade",
]

"""
SQLAlchemy ORM models package.
"""
from app.models.student import Student, User
from app.models.course import Course
from app.models.enrollment import Enrollment
from app.models.assignment import Assignment
from app.models.grade import Grade
from app.models.achievement import Achievement, StudentAchievement
from app.models.gamification import Badge, UserBadge, Submission

__all__ = [
    "Student",
    "User",
    "Course",
    "Enrollment",
    "Assignment",
    "Grade",
    "Achievement",
    "StudentAchievement",
    "Badge",
    "UserBadge",
    "Submission",
]

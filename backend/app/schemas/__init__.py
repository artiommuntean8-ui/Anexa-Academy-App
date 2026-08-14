"""
Pydantic schemas package for data validation and serialization.
"""
from app.schemas.student import StudentBase, StudentCreate, StudentUpdate, StudentResponse
from app.schemas.course import CourseBase, CourseCreate, CourseUpdate, CourseResponse
from app.schemas.assignment import AssignmentBase, AssignmentCreate, AssignmentUpdate, AssignmentResponse
from app.schemas.grade import GradeBase, GradeCreate, GradeUpdate, GradeResponse
from app.schemas.enrollment import EnrollmentBase, EnrollmentCreate, EnrollmentResponse
from app.schemas.dashboard import DashboardOverviewResponse
from app.schemas.auth import LoginRequest, RegisterRequest, Token, TokenSwagger, TokenPayload

__all__ = [
    "StudentBase",
    "StudentCreate",
    "StudentUpdate",
    "StudentResponse",
    "CourseBase",
    "CourseCreate",
    "CourseUpdate",
    "CourseResponse",
    "AssignmentBase",
    "AssignmentCreate",
    "AssignmentUpdate",
    "AssignmentResponse",
    "GradeBase",
    "GradeCreate",
    "GradeUpdate",
    "GradeResponse",
    "EnrollmentBase",
    "EnrollmentCreate",
    "EnrollmentResponse",
    "DashboardOverviewResponse",
    "LoginRequest",
    "RegisterRequest",
    "Token",
    "TokenSwagger",
    "TokenPayload",
]

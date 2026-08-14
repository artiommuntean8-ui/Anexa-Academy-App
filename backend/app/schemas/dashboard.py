from typing import List, Optional
from pydantic import BaseModel, ConfigDict
from app.schemas.student import StudentResponse
from app.schemas.course import CourseResponse
from app.schemas.assignment import AssignmentResponse
from app.schemas.grade import GradeResponse


class DashboardOverviewResponse(BaseModel):
    student: StudentResponse
    total_enrolled_courses: int
    total_credits: int
    average_grade: float
    enrolled_courses: List[CourseResponse]
    upcoming_assignments: List[AssignmentResponse]
    recent_grades: List[GradeResponse]

    model_config = ConfigDict(from_attributes=True)

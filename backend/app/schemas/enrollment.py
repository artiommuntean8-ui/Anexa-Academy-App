import datetime
from typing import Optional
from pydantic import BaseModel, ConfigDict
from app.schemas.course import CourseResponse


class EnrollmentBase(BaseModel):
    student_id: int
    course_id: int
    status: str = "active"


class EnrollmentCreate(EnrollmentBase):
    pass


class EnrollmentResponse(EnrollmentBase):
    id: int
    enrolled_at: datetime.datetime
    course: Optional[CourseResponse] = None

    model_config = ConfigDict(from_attributes=True)

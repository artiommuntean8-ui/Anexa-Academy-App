import datetime
from typing import Optional
from pydantic import BaseModel, ConfigDict


class CourseBase(BaseModel):
    code: str
    title: str
    description: Optional[str] = None
    instructor_name: str
    semester: int = 1
    credits: int = 5


class CourseCreate(CourseBase):
    pass


class CourseUpdate(BaseModel):
    code: Optional[str] = None
    title: Optional[str] = None
    description: Optional[str] = None
    instructor_name: Optional[str] = None
    semester: Optional[int] = None
    credits: Optional[int] = None


class CourseResponse(CourseBase):
    id: int
    created_at: datetime.datetime

    model_config = ConfigDict(from_attributes=True)

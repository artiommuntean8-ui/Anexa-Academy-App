import datetime
from typing import Optional
from pydantic import BaseModel, ConfigDict


class GradeBase(BaseModel):
    assignment_id: int
    student_id: int
    score: float
    feedback: Optional[str] = None


class GradeCreate(GradeBase):
    pass


class GradeUpdate(BaseModel):
    score: Optional[float] = None
    feedback: Optional[str] = None


class GradeResponse(GradeBase):
    id: int
    graded_at: datetime.datetime

    model_config = ConfigDict(from_attributes=True)

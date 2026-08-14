import datetime
from typing import Optional
from pydantic import BaseModel, ConfigDict


class AssignmentBase(BaseModel):
    course_id: int
    title: str
    description: Optional[str] = None
    max_score: float = 100.0
    due_date: Optional[datetime.datetime] = None


class AssignmentCreate(AssignmentBase):
    pass


class AssignmentUpdate(BaseModel):
    title: Optional[str] = None
    description: Optional[str] = None
    max_score: Optional[float] = None
    due_date: Optional[datetime.datetime] = None


class AssignmentResponse(AssignmentBase):
    id: int
    created_at: datetime.datetime

    model_config = ConfigDict(from_attributes=True)

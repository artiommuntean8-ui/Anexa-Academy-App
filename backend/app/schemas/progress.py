from typing import List
from pydantic import BaseModel, ConfigDict
from app.schemas.student import StudentResponse


class ModuleProgress(BaseModel):
    module_id: int
    module_code: str
    module_title: str
    total_lessons: int
    completed_lessons: int
    progress_percent: float

    model_config = ConfigDict(from_attributes=True)


class LessonStatus(BaseModel):
    lesson_id: int
    lesson_title: str
    module_id: int
    module_title: str
    is_completed: bool
    completed_at: str | None = None
    feedback: str | None = None

    model_config = ConfigDict(from_attributes=True)


class StudentProgressResponse(BaseModel):
    student: StudentResponse
    overall_progress_percent: float
    total_lessons: int
    completed_lessons: int
    modules: List[ModuleProgress]
    lessons: List[LessonStatus] = []

    model_config = ConfigDict(from_attributes=True)


class StudentProgressSummary(BaseModel):
    student_id: int
    student_code: str
    full_name: str
    overall_progress_percent: float
    completed_lessons: int
    total_lessons: int

    model_config = ConfigDict(from_attributes=True)

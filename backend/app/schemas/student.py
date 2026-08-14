import datetime
from typing import Optional
from pydantic import BaseModel, EmailStr, ConfigDict


class StudentBase(BaseModel):
    student_code: str
    full_name: str
    email: EmailStr
    role: str = "student"
    department: str = "Software Engineering"
    semester: int = 1
    is_active: bool = True


class StudentCreate(StudentBase):
    password: str


class StudentUpdate(BaseModel):
    student_code: Optional[str] = None
    full_name: Optional[str] = None
    email: Optional[EmailStr] = None
    password: Optional[str] = None
    role: Optional[str] = None
    department: Optional[str] = None
    semester: Optional[int] = None
    is_active: Optional[bool] = None


class StudentResponse(StudentBase):
    id: int
    created_at: datetime.datetime
    updated_at: Optional[datetime.datetime] = None

    model_config = ConfigDict(from_attributes=True)

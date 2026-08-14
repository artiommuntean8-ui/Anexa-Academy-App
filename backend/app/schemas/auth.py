from typing import Optional
from pydantic import BaseModel, EmailStr
from app.schemas.student import StudentResponse


class LoginRequest(BaseModel):
    email: EmailStr
    password: str


class RegisterRequest(BaseModel):
    student_code: str
    full_name: str
    email: EmailStr
    password: str
    department: str = "Software Engineering"
    semester: int = 1


class Token(BaseModel):
    access_token: str
    token_type: str = "bearer"
    user: StudentResponse


class TokenSwagger(BaseModel):
    access_token: str
    token_type: str = "bearer"


class TokenPayload(BaseModel):
    sub: Optional[str] = None
    role: Optional[str] = None
    exp: Optional[int] = None

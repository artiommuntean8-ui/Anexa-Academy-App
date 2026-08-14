from typing import Any
from fastapi import APIRouter, Depends, HTTPException, status
from fastapi.security import OAuth2PasswordRequestForm
from sqlalchemy.orm import Session

from app.db.session import get_db
from app.core.security import verify_password, get_password_hash, create_access_token
from app.models.student import Student
from app.schemas.auth import LoginRequest, RegisterRequest, Token, TokenSwagger
from app.schemas.student import StudentResponse
from app.api.deps import get_current_user

router = APIRouter()


@router.post("/login", response_model=Token, summary="Desktop Client Login (JSON)")
def login_json(
    login_data: LoginRequest,
    db: Session = Depends(get_db)
) -> Any:
    """
    Authenticate a student or admin via JSON payload.
    Returns access token and student profile.
    """
    student = db.query(Student).filter(Student.email == login_data.email).first()
    if not student or not verify_password(login_data.password, student.hashed_password):
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Incorrect email or password",
            headers={"WWW-Authenticate": "Bearer"},
        )
    if not student.is_active:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Inactive student account",
        )

    access_token = create_access_token(
        subject=student.id,
        extra_claims={"role": student.role, "email": student.email}
    )
    return {
        "access_token": access_token,
        "token_type": "bearer",
        "user": student,
    }


@router.post("/login/access-token", response_model=TokenSwagger, summary="Swagger OAuth2 Login Form")
def login_access_token(
    form_data: OAuth2PasswordRequestForm = Depends(),
    db: Session = Depends(get_db)
) -> Any:
    """
    OAuth2 compatible token login, for Swagger UI interactivity.
    `username` parameter represents the student email.
    """
    student = db.query(Student).filter(Student.email == form_data.username).first()
    if not student or not verify_password(form_data.password, student.hashed_password):
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Incorrect email or password"
        )
    if not student.is_active:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Inactive student account"
        )

    access_token = create_access_token(
        subject=student.id,
        extra_claims={"role": student.role, "email": student.email}
    )
    return {
        "access_token": access_token,
        "token_type": "bearer"
    }


@router.post("/register", response_model=Token, status_code=status.HTTP_201_CREATED, summary="Student Registration")
def register(
    register_in: RegisterRequest,
    db: Session = Depends(get_db)
) -> Any:
    """
    Register a new student account with hashed password.
    """
    if db.query(Student).filter(Student.student_code == register_in.student_code).first():
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=f"Student code '{register_in.student_code}' is already registered."
        )
    if db.query(Student).filter(Student.email == register_in.email).first():
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=f"Email '{register_in.email}' is already registered."
        )

    student = Student(
        student_code=register_in.student_code,
        full_name=register_in.full_name,
        email=register_in.email,
        hashed_password=get_password_hash(register_in.password),
        department=register_in.department,
        semester=register_in.semester,
        role="student",
        is_active=True
    )
    db.add(student)
    db.commit()
    db.refresh(student)

    access_token = create_access_token(
        subject=student.id,
        extra_claims={"role": student.role, "email": student.email}
    )
    return {
        "access_token": access_token,
        "token_type": "bearer",
        "user": student,
    }


@router.get("/me", response_model=StudentResponse, summary="Get Current Authenticated User")
def get_current_user_profile(
    current_user: Student = Depends(get_current_user)
) -> Any:
    """
    Returns the profile data of the currently logged-in student.
    """
    return current_user

import logging
from typing import Optional, List, Dict, Any
from fastapi import APIRouter, Depends, HTTPException, status
from pydantic import BaseModel, Field
from sqlalchemy.orm import Session

from app.db.session import get_db
from app.api.deps import get_current_user
from app.models.student import Student
from app.models.test_case import TestCase
from app.models.assignment import Assignment
from app.services import gamification_service
from app.services.docker_sandbox import sandbox_service, TestCaseItem

logger = logging.getLogger("app.api.gamification")
router = APIRouter()


# =====================================================================
# Request & Response Schemas
# =====================================================================

class LeaderboardEntry(BaseModel):
    rank: int
    user_id: int
    student_code: str
    full_name: str
    xp: int
    level: int
    streak_days: int
    badges_count: int


class BadgeResponse(BaseModel):
    id: int
    code: str
    title: str
    description: str
    icon_name: str
    xp_reward: int
    is_unlocked: bool
    unlocked_at: Optional[str] = None


class ProfileResponse(BaseModel):
    user_id: int
    student_code: str
    full_name: str
    xp: int
    level: int
    streak_days: int
    last_active_date: Optional[str] = None
    progress: Dict[str, Any]
    badges: List[BadgeResponse]
    unlocked_badges_count: int
    total_badges_count: int


class SubmitCodeRequest(BaseModel):
    code: str = Field(..., description="Codul sursă Python trimis de elev")
    exercise_id: int = Field(..., description="ID-ul exercițiului/temei (assignment_id)")
    user_id: Optional[int] = Field(default=None, description="ID-ul elevului (opțional dacă se folosește Bearer token)")


# =====================================================================
# Endpoints
# =====================================================================

@router.get("/leaderboard", response_model=List[LeaderboardEntry], summary="Topul elevilor sortați după XP")
def get_leaderboard(
    limit: int = 50,
    db: Session = Depends(get_db),
):
    """
    Returnează clasamentul general al elevilor ordonat descrescător după XP.
    Include poziția în clasament (rank), numele complet, nivelul, XP-ul și numărul de insigne obținute.
    """
    return gamification_service.get_leaderboard(db, limit=limit)


@router.get("/profile/{user_id}", response_model=ProfileResponse, summary="Profilul de gamification al unui utilizator")
def get_profile(
    user_id: int,
    db: Session = Depends(get_db),
):
    """
    Returnează profilul detaliat de gamification pentru un elev:
    XP curent, nivel, progres către următorul nivel (0-100%), streak și galeria de insigne (deblocate vs blocate).
    """
    try:
        return gamification_service.get_student_profile(db, user_id)
    except ValueError as e:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=str(e))


@router.post("/submit", summary="Validare și trimitere soluție cu acordare XP și Insigne")
def submit_solution(
    request: SubmitCodeRequest,
    db: Session = Depends(get_db),
):
    """
    Execută codul în Sandbox Docker pe baza cazurilor de test ale exercițiului.
    Dacă toate testele trec, acordă automat XP (+50 prima dată, +10 din prima încercare),
    actualizează streak-ul, verifică și deblochează insigne, și detectează Level Up.
    """
    assignment = db.query(Assignment).filter(Assignment.id == request.exercise_id).first()
    if not assignment:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"Exercițiul cu ID-ul {request.exercise_id} nu a fost găsit."
        )

    # Încărcăm test cases
    db_cases = db.query(TestCase).filter(TestCase.assignment_id == request.exercise_id).all()
    test_cases_items = [
        TestCaseItem(
            id=tc.id,
            input_data=tc.input_data or "",
            expected_output=tc.expected_output,
            is_hidden=bool(tc.is_hidden)
        )
        for tc in db_cases
    ]

    # Rulăm codul prin Docker Sandbox Runner
    suite_res = sandbox_service.run_test_cases(request.code, test_cases_items, timeout=3.5)

    # Calculăm timpul total sau mediu de execuție
    total_exec_time = sum(r.execution_time_ms for r in suite_res.results) if suite_res.results else 0.0

    # Dacă avem user_id specificat sau luăm primul student default
    target_user_id = request.user_id
    if not target_user_id:
        # Fallback la primul student din DB dacă nu este specificat
        first_student = db.query(Student).filter(Student.role == "student").first()
        if first_student:
            target_user_id = first_student.id

    gamification_result = None
    if target_user_id:
        gamification_result = gamification_service.record_submission_and_award_xp(
            db=db,
            student_id=target_user_id,
            assignment_id=request.exercise_id,
            code=request.code,
            passed=suite_res.all_passed,
            execution_time_ms=total_exec_time,
        )

    return {
        "status": "success" if suite_res.all_passed else "failed",
        "all_passed": suite_res.all_passed,
        "score": suite_res.score,
        "passed_count": suite_res.passed_count,
        "total_count": suite_res.total_count,
        "results": [r.model_dump() for r in suite_res.results],
        "runner": suite_res.runner,
        "gamification": gamification_result,
        # Helper fields direct în root pentru consum rapid de către clienți
        "xp_awarded": gamification_result.get("xp_awarded", 0) if gamification_result else 0,
        "total_xp": gamification_result.get("total_xp", 0) if gamification_result else 0,
        "level": gamification_result.get("level", 1) if gamification_result else 1,
        "level_up": gamification_result.get("level_up", False) if gamification_result else False,
        "new_level": gamification_result.get("new_level", 1) if gamification_result else 1,
        "newly_unlocked_badges": gamification_result.get("newly_unlocked_badges", []) if gamification_result else [],
    }

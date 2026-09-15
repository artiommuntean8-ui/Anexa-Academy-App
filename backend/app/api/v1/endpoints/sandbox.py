import logging
from typing import Optional, List
from fastapi import APIRouter, Depends, HTTPException, status
from pydantic import BaseModel, Field
from sqlalchemy.orm import Session

from app.db.session import get_db
from app.models.test_case import TestCase
from app.models.grade import Grade
from app.models.student import Student
from app.services.docker_sandbox import (
    sandbox_service,
    ExecutionResult,
    TestCaseItem,
    TestSuiteResult,
)

logger = logging.getLogger("app.api.sandbox")
router = APIRouter()


# =====================================================================
# Request Schemas
# =====================================================================

class CodeRunRequest(BaseModel):
    """Schema cererii pentru rularea unui script de cod în sandbox."""
    code: str = Field(..., description="Codul sursă Python de executat")
    input_data: Optional[str] = Field(default="", description="Date transmise către sys.stdin")
    timeout: Optional[float] = Field(default=3.5, ge=1.0, le=10.0, description="Timp maxim de execuție în secunde (3-5s recomandat)")


class SingleTestCase(BaseModel):
    """Schema unui caz de test specificat direct în request."""
    id: Optional[int] = None
    input_data: Optional[str] = ""
    expected_output: str
    is_hidden: Optional[bool] = False


class CodeTestRequest(BaseModel):
    """Schema cererii pentru validarea codului împotriva testelor."""
    code: str = Field(..., description="Codul sursă Python de testat")
    exercise_id: Optional[int] = Field(default=None, description="ID-ul exercițiului/temei pentru încărcare teste din DB")
    test_cases: Optional[List[SingleTestCase]] = Field(default=None, description="Listă manuală de cazuri de test")
    timeout: Optional[float] = Field(default=3.5, ge=1.0, le=10.0, description="Timeout per caz de test")


# =====================================================================
# Endpoints
# =====================================================================

@router.post("/run", response_model=ExecutionResult, summary="Rulează cod Python în Sandbox Docker")
def run_code(request: CodeRunRequest) -> ExecutionResult:
    """
    Execută un fragment de cod Python într-un container ephemer Docker (sau fallback securizat dacă Docker nu rulează).
    Limitează memoria la 128MB, CPU la 0.5 nuclee, dezactivează rețeaua și forțează timeout după 3-5 secunde.
    """
    return sandbox_service.run_code(
        code=request.code,
        input_data=request.input_data or "",
        timeout=request.timeout,
    )


@router.post("/test", response_model=TestSuiteResult, summary="Testează cod Python împotriva unei suite de teste")
def test_code(
    request: CodeTestRequest,
    db: Session = Depends(get_db),
) -> TestSuiteResult:
    """
    Rulează codul împotriva unei liste de cazuri de test (fie furnizate direct în request, fie extrase din baza de date pentru un exercise_id).
    Fiecare test rulează cu stdin-ul setat la input_data corespunzător și compară ieșirea cu expected_output.
    """
    cases_to_run: List[TestCaseItem] = []

    if request.test_cases:
        cases_to_run = [
            TestCaseItem(
                id=tc.id,
                input_data=tc.input_data or "",
                expected_output=tc.expected_output,
                is_hidden=bool(tc.is_hidden),
            )
            for tc in request.test_cases
        ]
    elif request.exercise_id:
        db_cases = db.query(TestCase).filter(TestCase.assignment_id == request.exercise_id).all()
        if not db_cases:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail=f"Nu s-au găsit cazuri de test pentru exercițiul {request.exercise_id}",
            )
        cases_to_run = [
            TestCaseItem(
                id=tc.id,
                input_data=tc.input_data or "",
                expected_output=tc.expected_output,
                is_hidden=bool(tc.is_hidden),
            )
            for tc in db_cases
        ]
    else:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Trebuie furnizat fie 'test_cases', fie 'exercise_id'.",
        )

    return sandbox_service.run_test_cases(
        code=request.code,
        test_cases=cases_to_run,
        timeout=request.timeout,
    )


@router.get("/status", summary="Starea serviciului Docker Sandbox")
def get_sandbox_status():
    """
    Verifică disponibilitatea Docker Daemon pe server.
    """
    is_docker = sandbox_service.is_docker_available()
    return {
        "status": "ready",
        "docker_available": is_docker,
        "active_runner": "docker" if is_docker else "fallback_secure_local",
        "limits": {
            "memory": sandbox_service.mem_limit,
            "nano_cpus": sandbox_service.nano_cpus,
            "network_disabled": sandbox_service.network_disabled,
            "user": sandbox_service.user,
            "read_only": sandbox_service.read_only,
            "tmpfs": sandbox_service.tmpfs,
            "auto_remove": sandbox_service.auto_remove,
            "default_timeout_s": sandbox_service.default_timeout,
        },
    }


class SandboxSubmitRequest(BaseModel):
    code: str
    exercise_id: int
    user_id: Optional[int] = None
    timeout: Optional[float] = 3.5


@router.post("/submit", summary="Trimitere soluție cu validare automată și acordare Gamification")
def submit_code(
    request: SandboxSubmitRequest,
    db: Session = Depends(get_db),
):
    """
    Execută codul în Sandbox și acordă XP, actualizează streak-ul și deblochează insigne dacă testele trec.
    """
    from app.services import gamification_service
    from app.models.assignment import Assignment

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

    suite_res = sandbox_service.run_test_cases(request.code, test_cases_items, timeout=request.timeout)
    total_exec_time = sum(r.execution_time_ms for r in suite_res.results) if suite_res.results else 0.0

    target_user_id = request.user_id
    if not target_user_id:
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
        "xp_awarded": gamification_result.get("xp_awarded", 0) if gamification_result else 0,
        "total_xp": gamification_result.get("total_xp", 0) if gamification_result else 0,
        "level": gamification_result.get("level", 1) if gamification_result else 1,
        "level_up": gamification_result.get("level_up", False) if gamification_result else False,
        "new_level": gamification_result.get("new_level", 1) if gamification_result else 1,
        "newly_unlocked_badges": gamification_result.get("newly_unlocked_badges", []) if gamification_result else [],
    }


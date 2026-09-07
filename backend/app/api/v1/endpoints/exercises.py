import sys
import io
import contextlib
from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from app.db.session import get_db
from app.api.deps import get_current_user
from app.models.grade import Grade

router = APIRouter()


def _run_student_code_safely(code: str) -> dict:
    """Execută codul elevului într-un mediu controlat cu captură de stdout."""
    stdout = io.StringIO()
    # Safe restricted builtins
    safe_builtins = {
        'print': print,
        'range': range,
        'len': len,
        'str': str,
        'int': int,
        'float': float,
        'bool': bool,
        'list': list,
        'dict': dict,
        'set': set,
        'tuple': tuple,
        'sum': sum,
        'min': min,
        'max': max,
        'abs': abs,
        'round': round,
        'enumerate': enumerate,
        'zip': zip,
        'sorted': sorted,
        'reversed': reversed,
    }

    try:
        with contextlib.redirect_stdout(stdout):
            local_scope = {}
            exec(code, {'__builtins__': safe_builtins}, local_scope)
        output_text = stdout.getvalue()
        return {"status": "success", "output": output_text}
    except Exception as e:
        return {"status": "error", "output": str(e)}


@router.post("/validate")
def validate_code(
    data: dict,
    db: Session = Depends(get_db),
    current_user = Depends(get_current_user)
):
    code = data.get("code", "")
    exercise_id = data.get("exercise_id")

    if not code.strip():
        return {"status": "error", "message": "Codul trimis este gol. Scrie o soluție înainte de trimitere."}

    result = _run_student_code_safely(code)

    if result["status"] == "success":
        output = result.get("output", "")
        # Auto-grade assignment if exercise_id provided
        if exercise_id:
            try:
                ex_id_int = int(exercise_id)
                existing_grade = db.query(Grade).filter(
                    Grade.student_id == current_user.id,
                    Grade.assignment_id == ex_id_int
                ).first()
                if not existing_grade:
                    db.add(Grade(
                        student_id=current_user.id,
                        assignment_id=ex_id_int,
                        score=100.0,
                        feedback="Exercițiu rezolvat și validat cu succes prin consola interactivă!"
                    ))
                    db.commit()
            except Exception:
                pass

        return {
            "status": "success",
            "message": f"Codul a rulat cu succes!\n\nIeșire consolă:\n{output if output else '(Fără text afișat)'}",
            "output": output
        }

    return {
        "status": "error",
        "message": f"Eroare de execuție: {result.get('output')}"
    }

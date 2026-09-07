import sys
import io
import json
import contextlib
import traceback
from typing import List, Dict, Any, Optional
from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from app.db.session import get_db
from app.api.deps import get_current_user
from app.models.student import Student
from app.models.assignment import Assignment
from app.models.grade import Grade
from app.models.achievement import Achievement, StudentAchievement

router = APIRouter()


def _get_pedagogical_hint(error_name: str, error_msg: str, code: str) -> str:
    """Generates helpful, friendly explanations in Romanian for common Python errors."""
    if "IndentationError" in error_name:
        return "💡 Indiciu ArkiTech: În Python, spațiile de la începutul rândului (indentarea) sunt foarte importante! Asigură-te că liniile din interiorul funcțiilor sau buclelor sunt aliniate cu 4 spații sau o tastă Tab."
    elif "NameError" in error_name:
        return "💡 Indiciu ArkiTech: Se pare că ai folosit o variabilă sau funcție care nu a fost definită anterior. Verifică dacă ai scris corect numele variabilei (fără greșeli de literă)."
    elif "TypeError" in error_name:
        return "💡 Indiciu ArkiTech: Ai încercat o operație între tipuri de date incompatibile (de exemplu, adunarea unui număr cu un text). Folosește str() sau int() pentru conversie."
    elif "IndexError" in error_name:
        return "💡 Indiciu ArkiTech: Ai încercat să accesezi o poziție din listă care nu există. Amintește-ți că indexarea în Python începe de la 0!"
    elif "ZeroDivisionError" in error_name:
        return "💡 Indiciu ArkiTech: Împărțirea la zero nu este permisă în matematică sau programare! Verifică valorile numitorului."
    elif "SyntaxError" in error_name:
        return "💡 Indiciu ArkiTech: Există o greșeală de sintaxă. Verifică dacă ai închis toate parantezele '()', ghilimelele '\"' și dacă ai pus două puncte ':' la finalul instrucțiunilor if/for/def."
    return f"💡 Indiciu ArkiTech: Verifică logica codului. Detalii eroare: {error_msg}"


def _execute_code_sandbox(code: str) -> Dict[str, Any]:
    """Runs code in a clean namespace with stdout redirection."""
    stdout_buf = io.StringIO()
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
        'type': type,
        'isinstance': isinstance,
        'True': True,
        'False': False,
        'None': None,
    }

    local_scope: Dict[str, Any] = {}
    try:
        with contextlib.redirect_stdout(stdout_buf):
            exec(code, {'__builtins__': safe_builtins}, local_scope)
        return {
            "success": True,
            "stdout": stdout_buf.getvalue(),
            "scope": local_scope,
            "error_type": None,
            "error_message": None
        }
    except Exception as e:
        return {
            "success": False,
            "stdout": stdout_buf.getvalue(),
            "scope": local_scope,
            "error_type": type(e).__name__,
            "error_message": str(e)
        }


def _evaluate_test_cases(code: str, test_cases: List[Dict[str, Any]]) -> Dict[str, Any]:
    """Evaluates student code against unit test cases."""
    # 1. First run the main script to define functions/classes
    run_res = _execute_code_sandbox(code)
    if not run_res["success"]:
        hint = _get_pedagogical_hint(run_res["error_type"], run_res["error_message"], code)
        return {
            "passed": False,
            "score": 0.0,
            "stdout": run_res["stdout"],
            "test_results": [],
            "error": f"{run_res['error_type']}: {run_res['error_message']}",
            "hint": hint
        }

    scope = run_res["scope"]
    stdout_output = run_res["stdout"]
    test_results = []
    passed_count = 0

    for idx, test in enumerate(test_cases, start=1):
        test_type = test.get("type", "call")
        desc = test.get("description", f"Test #{idx}")
        expected = test.get("expected")

        if test_type == "stdout_contains":
            target = str(expected).strip()
            passed = target.lower() in stdout_output.lower()
            test_results.append({
                "index": idx,
                "name": desc,
                "type": "stdout",
                "expected": f"Conține textul: '{target}'",
                "actual": stdout_output.strip() if stdout_output else "(Fără text)",
                "passed": passed
            })
            if passed:
                passed_count += 1

        elif test_type == "call":
            call_expr = test.get("call", "")
            try:
                actual_val = eval(call_expr, {"__builtins__": {}}, scope)
                passed = actual_val == expected
                test_results.append({
                    "index": idx,
                    "name": desc or call_expr,
                    "type": "call",
                    "call": call_expr,
                    "expected": str(expected),
                    "actual": str(actual_val),
                    "passed": passed
                })
                if passed:
                    passed_count += 1
            except Exception as e:
                test_results.append({
                    "index": idx,
                    "name": desc or call_expr,
                    "type": "call",
                    "call": call_expr,
                    "expected": str(expected),
                    "actual": f"Eroare execuție apel: {type(e).__name__} ({str(e)})",
                    "passed": False
                })

    total_tests = len(test_cases)
    score = (passed_count / total_tests * 100.0) if total_tests > 0 else 100.0
    all_passed = passed_count == total_tests

    hint = None
    if not all_passed:
        hint = "💡 Unele teste nu au produs rezultatul așteptat. Verifică valorile returnate pentru toate cazurile de test."

    return {
        "passed": all_passed,
        "score": score,
        "passed_count": passed_count,
        "total_tests": total_tests,
        "stdout": stdout_output,
        "test_results": test_results,
        "error": None,
        "hint": hint
    }


def _check_and_award_achievements(db: Session, student_id: int, code: str, score: float) -> List[Dict[str, Any]]:
    """Checks for newly unlocked achievements and records them."""
    newly_unlocked = []

    def award_if_not_unlocked(code_str: str):
        ach = db.query(Achievement).filter(Achievement.code == code_str).first()
        if not ach:
            return
        exists = db.query(StudentAchievement).filter(
            StudentAchievement.student_id == student_id,
            StudentAchievement.achievement_id == ach.id
        ).first()
        if not exists:
            db.add(StudentAchievement(student_id=student_id, achievement_id=ach.id))
            db.commit()
            newly_unlocked.append({
                "id": ach.id,
                "code": ach.code,
                "title": ach.title,
                "description": ach.description,
                "icon": ach.icon,
                "xp_reward": ach.xp_reward
            })

    # 1. FIRST_CODE (Any successful run)
    award_if_not_unlocked("FIRST_CODE")

    # 2. PERFECT_SCORE (100% score)
    if score >= 100.0:
        award_if_not_unlocked("PERFECT_SCORE")

    # 3. LOOP_MASTER (Contains for or while)
    if "for " in code or "while " in code:
        award_if_not_unlocked("LOOP_MASTER")

    # 4. FUNCTION_PRO (Contains def)
    if "def " in code:
        award_if_not_unlocked("FUNCTION_PRO")

    # 5. DATA_WIZARD (Contains lists or dicts syntax)
    if ("[" in code and "]" in code) or ("{" in code and "}" in code):
        award_if_not_unlocked("DATA_WIZARD")

    # 6. TRIPLE_CROWN (Completed 3 or more graded assignments)
    grades_count = db.query(Grade).filter(Grade.student_id == student_id, Grade.score >= 80.0).count()
    if grades_count >= 3:
        award_if_not_unlocked("TRIPLE_CROWN")

    return newly_unlocked


@router.post("/validate", summary="Auto-Grader runner with unit tests and gamification")
def validate_code(
    data: dict,
    db: Session = Depends(get_db),
    current_user: Student = Depends(get_current_user)
):
    code = data.get("code", "")
    exercise_id = data.get("exercise_id")

    if not code or not code.strip():
        return {
            "status": "error",
            "message": "Codul trimis este gol. Scrie o soluție înainte de verificare.",
            "test_results": [],
            "score": 0.0,
            "unlocked_achievements": []
        }

    test_cases: List[Dict[str, Any]] = []
    if exercise_id:
        try:
            assignment = db.query(Assignment).filter(Assignment.id == int(exercise_id)).first()
            if assignment and assignment.test_cases:
                test_cases = json.loads(assignment.test_cases)
        except Exception:
            test_cases = []

    # If test cases exist, run full unit testing
    if test_cases:
        eval_res = _evaluate_test_cases(code, test_cases)
    else:
        # Generic run
        run_res = _execute_code_sandbox(code)
        if run_res["success"]:
            eval_res = {
                "passed": True,
                "score": 100.0,
                "passed_count": 1,
                "total_tests": 1,
                "stdout": run_res["stdout"],
                "test_results": [
                    {
                        "index": 1,
                        "name": "Execuție fără erori de sintaxă/runtime",
                        "type": "generic",
                        "expected": "Execuție cu succes",
                        "actual": "Codul a rulat fără excepții",
                        "passed": True
                    }
                ],
                "error": None,
                "hint": None
            }
        else:
            hint = _get_pedagogical_hint(run_res["error_type"], run_res["error_message"], code)
            eval_res = {
                "passed": False,
                "score": 0.0,
                "passed_count": 0,
                "total_tests": 1,
                "stdout": run_res["stdout"],
                "test_results": [
                    {
                        "index": 1,
                        "name": "Execuție cod Python",
                        "type": "generic",
                        "expected": "Fără erori",
                        "actual": f"{run_res['error_type']}: {run_res['error_message']}",
                        "passed": False
                    }
                ],
                "error": f"{run_res['error_type']}: {run_res['error_message']}",
                "hint": hint
            }

    score = eval_res["score"]
    all_passed = eval_res["passed"]
    newly_unlocked = []

    # Record grade & award achievements if exercise_id given and passed
            # Record grade & award achievements if exercise_id given and passed
            if exercise_id and all_passed:
                try:
                    ex_id_int = int(exercise_id)
                    existing_grade = db.query(Grade).filter(
                        Grade.student_id == current_user.id,
                        Grade.assignment_id == ex_id_int
                    ).first()

                    if not existing_grade:
                        existing_grade = Grade(
                            student_id=current_user.id,
                            assignment_id=ex_id_int,
                            score=score,
                            feedback="Toate testele automate au fost validate cu succes (Auto-Grader 100%)."
                        )
                        db.add(existing_grade)
                        db.commit()
                    else:
                        existing_grade.score = max(existing_grade.score, score)
                        db.commit()

                    # Award achievements
                    newly_unlocked = _check_and_award_achievements(db, current_user.id, code, score)

                except Exception as e:
                    print(f"Error updating grade/achievements: {e}")

            # Salvează încercarea în history (chiar dacă a eșuat sau reușit)
            if exercise_id:
                from sqlalchemy import text
                import datetime
                db.execute(
                    text("INSERT INTO attempt_history (grade_id, code, timestamp, feedback) VALUES (:g, :c, :t, :f)"),
                    {
                        "g": existing_grade.id if 'existing_grade' in locals() and existing_grade else 0,
                        "c": code,
                        "t": datetime.datetime.utcnow(),
                        "f": eval_res.get("error") if not all_passed else "Success"
                    }
                )
                db.commit()

    if exercise_id and all_passed:
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
                    score=score,
                    feedback="Toate testele automate au fost validate cu succes (Auto-Grader 100%)."
                ))
                db.commit()
            else:
                existing_grade.score = max(existing_grade.score, score)
                db.commit()

            # Award achievements
            newly_unlocked = _check_and_award_achievements(db, current_user.id, code, score)

        except Exception as e:
            print(f"Error updating grade/achievements: {e}")

    return {
        "status": "success" if all_passed else "failed",
        "score": score,
        "passed": all_passed,
        "stdout": eval_res.get("stdout", ""),
        "test_results": eval_res.get("test_results", []),
        "error": eval_res.get("error"),
        "hint": eval_res.get("hint"),
        "unlocked_achievements": newly_unlocked,
        "message": "🎉 Excelent! Toate testele au trecut cu succes!" if all_passed else "⚠️ Unele teste au eșuat. Verifică indiciile de mai jos."
    }

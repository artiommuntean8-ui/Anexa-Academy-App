import sys
import io
import contextlib
import multiprocessing
from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from app.db.session import get_db
from app.api.deps import get_current_user
from app.models.student import Student
from app.models.grade import Grade
from app.models.test_case import TestCase
from typing import List, Dict, Any

router = APIRouter()

def _execute_code_sandbox(code: str) -> Dict[str, Any]:
    stdout_buf = io.StringIO()
    safe_builtins = {
        'print': print, 'range': range, 'len': len, 'str': str, 
        'int': int, 'float': float, 'bool': bool
    }
    local_scope: Dict[str, Any] = {}
    try:
        with contextlib.redirect_stdout(stdout_buf):
            exec(code, {'__builtins__': safe_builtins}, local_scope)
        return {'success': True, 'stdout': stdout_buf.getvalue()}
    except Exception as e:
        return {'success': False, 'stdout': stdout_buf.getvalue(), 'error': str(e)}

@router.post('/validate')
def validate_code(
    data: dict,
    db: Session = Depends(get_db),
    current_user: Student = Depends(get_current_user)
):
    code = data.get('code', '')
    exercise_id = data.get('exercise_id')
    
    test_cases = db.query(TestCase).filter(TestCase.assignment_id == exercise_id).all()
    results = []
    all_passed = True
    
    for tc in test_cases:
        run_res = _execute_code_sandbox(code)
        passed = run_res['success'] and run_res['stdout'].strip() == tc.expected_output.strip()
        
        results.append({
            'test_id': tc.id,
            'status': 'PASSED' if passed else 'FAILED',
            'is_hidden': tc.is_hidden,
            'expected': tc.expected_output if not tc.is_hidden else 'HIDDEN',
            'got': run_res['stdout'].strip() if not tc.is_hidden else 'HIDDEN'
        })
        if not passed:
            all_passed = False
            
    if all_passed:
        existing_grade = db.query(Grade).filter(
            Grade.student_id == current_user.id, 
            Grade.assignment_id == exercise_id
        ).first()
        
        if not existing_grade:
            db.add(Grade(student_id=current_user.id, assignment_id=exercise_id, score=100.0))
            db.commit()
            
    return {'passed': all_passed, 'results': results}

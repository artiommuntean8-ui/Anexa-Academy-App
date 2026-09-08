import sys
import io
import contextlib
import bdb
from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from app.db.session import get_db
from app.api.deps import get_current_user
from app.models.student import Student
from app.models.grade import Grade
from app.models.test_case import TestCase
from typing import List, Dict, Any

router = APIRouter()

class TraceDebugger(bdb.Bdb):
    def __init__(self):
        super().__init__()
        self.trace_data = []

    def user_line(self, frame):
        line_no = frame.f_lineno
        locals_copy = {k: str(v) for k, v in frame.f_locals.items() if not k.startswith('__')}
        self.trace_data.append({'line': line_no, 'vars': locals_copy})

def _execute_code_with_trace(code: str) -> Dict[str, Any]:
    debugger = TraceDebugger()
    try:
        debugger.run(code)
        return {'success': True, 'trace': debugger.trace_data}
    except Exception as e:
        return {'success': False, 'error': str(e)}

@router.post('/trace')
def trace_code(
    data: dict,
    current_user: Student = Depends(get_current_user)
):
    return _execute_code_with_trace(data.get('code', ''))

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

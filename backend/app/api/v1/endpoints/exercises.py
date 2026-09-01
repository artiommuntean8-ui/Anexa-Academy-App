import sys
import io
import contextlib
import multiprocessing
from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from app.db.session import get_db
from app.api.deps import get_current_user
from app.models.grade import Grade

router = APIRouter()

def _run_student_code(code: str, queue: multiprocessing.Queue):
    """Execută codul elevului într-un proces izolat."""
    stdout = io.StringIO()
    try:
        with contextlib.redirect_stdout(stdout):
            # Sandbox limitat
            exec(code, {'__builtins__': {
                'print': print,
                'range': range,
                'len': len,
                'str': str,
                'int': int
            }})
        queue.put({"status": "success", "output": stdout.getvalue()})
    except Exception as e:
        queue.put({"status": "error", "output": str(e)})

@router.post("/validate")
def validate_code(
    data: dict,
    db: Session = Depends(get_db),
    current_user = Depends(get_current_user)
):
    code = data.get("code", "")
    exercise_id = data.get("exercise_id")
    
    # Executăm codul într-un proces separat pentru siguranță
    queue = multiprocessing.Queue()
    p = multiprocessing.Process(target=_run_student_code, args=(code, queue))
    p.start()
    p.join(timeout=5)  # Timeout de 5 secunde
    
    if p.is_alive():
        p.terminate()
        return {"status": "error", "message": "Codul a rulat prea mult (timeout)."}
    
    result = queue.get()
    
    if result["status"] == "success":
        # Logica de notare automată dacă output-ul conține ceva
        if "Salut" in result["output"] or "Hello" in result["output"]:
            return {"status": "success", "message": f"Bravo! Output: {result['output']}"}
        return {"status": "error", "message": f"Codul a rulat, dar output-ul nu e cel așteptat: {result['output']}"}
    
    return {"status": "error", "message": f"Eroare: {result['output']}"}

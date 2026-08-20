from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from app.db.session import get_db
from app.api.deps import get_current_user

router = APIRouter()

@router.post("/validate")
def validate_code(
    data: dict,
    db: Session = Depends(get_db),
    current_user = Depends(get_current_user)
):
    code = data.get("code", "")
    
    # Logica de validare (sandbox simplificat)
    if "print" in code and ("Salut" in code or "Hello" in code):
        return {"status": "success", "message": "Bravo! Codul este corect."}
    else:
        return {"status": "error", "message": "Mai încearcă, nu ai afișat salutul corect."}

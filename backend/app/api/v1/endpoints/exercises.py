from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from app.db.session import get_db
from app.api.deps import get_current_user
from app.models.assignment import Assignment
from app.models.grade import Grade

router = APIRouter()

@router.post("/validate")
def validate_code(
    data: dict,
    db: Session = Depends(get_db),
    current_user = Depends(get_current_user)
):
    code = data.get("code", "")
    exercise_id = data.get("exercise_id")
    
    # 1. Verificare sintaxă de bază
    try:
        compile(code, '<string>', 'exec')
    except SyntaxError as e:
        return {"status": "error", "message": f"Eroare de sintaxă: {str(e)}"}

    # 2. Logica de validare (exemplu logic)
    if "print" in code and ("Salut" in code or "Hello" in code):
        # 3. Salvare progres (Exemplu: dacă nu există notă, adăugăm una)
        existing_grade = db.query(Grade).filter(
            Grade.student_id == current_user.id, 
            Grade.assignment_id == exercise_id
        ).first()
        
        if not existing_grade:
            new_grade = Grade(student_id=current_user.id, assignment_id=exercise_id, score=100.0)
            db.add(new_grade)
            db.commit()
            
        return {"status": "success", "message": "Bravo! Ai terminat tema."}
    
    return {"status": "error", "message": "Mai încearcă, nu ai afișat salutul corect."}

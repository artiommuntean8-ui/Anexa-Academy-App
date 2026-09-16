from fastapi import APIRouter, Depends
from fastapi.responses import StreamingResponse
from sqlalchemy.orm import Session
from app.db.session import get_db
from app.services.pdf_report_service import ReportPDF
import io

router = APIRouter()

@router.get('/student/{student_id}/pdf')
def get_student_report(student_id: int, db: Session = Depends(get_db)):
    # Simulare date pentru PDF
    pdf = ReportPDF()
    pdf_data = pdf.generate_report('Elev Demo', 450, 5, 85, {'Python Basic': 'Insu?it', 'Bucle': 'In lucru'})
    
    return StreamingResponse(io.BytesIO(pdf_data), media_type='application/pdf')

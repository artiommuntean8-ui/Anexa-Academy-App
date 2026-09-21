from fastapi import APIRouter, Depends, HTTPException, status
from fastapi.responses import StreamingResponse
from sqlalchemy.orm import Session
from app.db.session import get_db
from app.services.pdf_report_service import ReportPDF
from app.services.progress import build_student_progress
from app.models.student import Student
import io
import logging

logger = logging.getLogger("app.api.reports")
router = APIRouter()


@router.get("/student/{student_id}/pdf")
def get_student_report(student_id: int, db: Session = Depends(get_db)):
    try:
        student = db.query(Student).filter(Student.id == student_id).first()
        if not student:
            raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Student not found")

        progress = build_student_progress(db, student)
        modules = {
            item.get("module_title", "Modul"): f"{item.get('progress_percent', 0)}%"
            for item in progress.get("modules", [])
        }
        pdf = ReportPDF()
        pdf_data = pdf.generate_report(
            student.full_name,
            student.xp or 0,
            student.level or 1,
            progress.get("overall_progress_percent", 0),
            modules,
        )
        filename = f"raport_elev_{student_id}.pdf"
        return StreamingResponse(
            io.BytesIO(pdf_data),
            media_type="application/pdf",
            headers={"Content-Disposition": f'attachment; filename="{filename}"'},
        )
    except HTTPException:
        raise
    except Exception as e:
        logger.error(f"Error generating PDF report for student {student_id}: {e}")
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Eroare la generarea raportului PDF: {str(e)}"
        )

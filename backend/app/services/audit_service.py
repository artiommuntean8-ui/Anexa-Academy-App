from sqlalchemy.orm import Session
from app.models.audit_log import AuditLog
import datetime

def log_audit_event(db: Session, user_id: int, event_type: str, details: dict = None, ip_address: str = '127.0.0.1'):
    log = AuditLog(
        user_id=user_id,
        event_type=event_type,
        details=details,
        ip_address=ip_address,
        created_at=datetime.datetime.utcnow()
    )
    db.add(log)
    db.commit()
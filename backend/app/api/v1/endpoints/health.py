from typing import Any, Dict
from fastapi import APIRouter
from app.core.config import settings

router = APIRouter()


@router.get("/health", response_model=Dict[str, Any], summary="Health Check")
def health_check() -> Dict[str, Any]:
    """
    Check the health and operational status of the API.
    """
    return {
        "status": "healthy",
        "project": settings.PROJECT_NAME,
        "version": settings.VERSION,
    }

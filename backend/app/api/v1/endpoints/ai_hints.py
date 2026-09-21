from fastapi import APIRouter, Depends, HTTPException, status
from app.services.ai_service import get_socratic_hint
from app.api.deps import get_current_user
import logging

logger = logging.getLogger("app.api.ai_hints")
router = APIRouter()

@router.post('/hint')
async def request_hint(data: dict, current_user=Depends(get_current_user)):
    try:
        code = data.get('code', '')
        error = data.get('error_log', '')
        hint_count = data.get('hint_count', 0)

        hint = await get_socratic_hint(code, error, hint_count)
        return {'hint_message': hint, 'remaining_hints': max(0, 3 - hint_count - 1)}
    except HTTPException:
        raise
    except Exception as e:
        logger.error(f"Error generating AI hint: {e}")
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Eroare la generarea indiciului: {str(e)}"
        )

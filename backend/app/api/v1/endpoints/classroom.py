from fastapi import APIRouter, WebSocket, WebSocketDisconnect
from app.services.classroom_ws import manager

router = APIRouter()

@router.websocket('/ws/{role}/{student_id}')
async def classroom_ws(websocket: WebSocket, role: str, student_id: int):
    if role == 'instructor':
        await manager.connect_instructor(websocket)
    else:
        await manager.connect_student(websocket, student_id, f'Elev {student_id}')
    
    try:
        while True:
            data = await websocket.receive_json()
            if data.get('type') == 'raise_hand':
                await manager.notify_instructors({
                    'type': 'hand_raised',
                    'student_id': student_id,
                    'task': data.get('task')
                })
    except WebSocketDisconnect:
        if role != 'instructor':
            manager.disconnect_student(student_id)

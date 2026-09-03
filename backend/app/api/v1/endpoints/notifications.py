from fastapi import APIRouter, WebSocket, WebSocketDisconnect, Depends
from sqlalchemy.orm import Session
from app.db.session import get_db
from app.api.deps import get_current_user
from app.models.student import Student
from typing import List

router = APIRouter()

class ConnectionManager:
    def __init__(self):
        self.active_connections: List[WebSocket] = []

    async def connect(self, websocket: WebSocket):
        await websocket.accept()
        self.active_connections.append(websocket)

    def disconnect(self, websocket: WebSocket):
        self.active_connections.remove(websocket)

    async def broadcast(self, message: str):
        for connection in self.active_connections:
            await connection.send_text(message)

manager = ConnectionManager()

@router.websocket('/ws/{client_id}')
async def websocket_endpoint(websocket: WebSocket, client_id: int):
    await manager.connect(websocket)
    try:
        while True:
            data = await websocket.receive_text()
            await manager.broadcast(f'Client #{client_id} says: {data}')
    except WebSocketDisconnect:
        manager.disconnect(websocket)
        await manager.broadcast(f'Client #{client_id} left the chat')

@router.get('/unread-count', summary='Get number of pending assignments')
def get_unread_count(
    db: Session = Depends(get_db),
    current_user: Student = Depends(get_current_user)
):
    from app.models.assignment import Assignment
    from app.models.grade import Grade
    
    total_assignments = db.query(Assignment).count()
    graded_assignments = db.query(Grade).filter(Grade.student_id == current_user.id).count()
    
    return {'unread': max(0, total_assignments - graded_assignments)}

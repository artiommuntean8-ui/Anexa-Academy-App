from fastapi import WebSocket
from typing import Dict, List

class ClassroomManager:
    def __init__(self):
        self.active_students: Dict[int, Dict] = {}
        self.instructor_connections: List[WebSocket] = []

    async def connect_student(self, websocket: WebSocket, student_id: int, name: str):
        await websocket.accept()
        self.active_students[student_id] = {
            'websocket': websocket, 
            'name': name, 
            'status': 'Online', 
            'current_task': 'None'
        }
        await self.notify_instructors({'type': 'student_joined', 'student_id': student_id, 'name': name})

    async def connect_instructor(self, websocket: WebSocket):
        await websocket.accept()
        self.instructor_connections.append(websocket)

    def disconnect_student(self, student_id: int):
        if student_id in self.active_students:
            del self.active_students[student_id]

    async def notify_instructors(self, data: dict):
        for ws in self.instructor_connections:
            await ws.send_json(data)

    async def update_student_status(self, student_id: int, status: str, task: str = None):
        if student_id in self.active_students:
            self.active_students[student_id]['status'] = status
            if task:
                self.active_students[student_id]['current_task'] = task
            
            await self.notify_instructors({
                'type': 'status_update',
                'student_id': student_id,
                'status': status,
                'task': self.active_students[student_id]['current_task']
            })

manager = ClassroomManager()

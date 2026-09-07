from PySide6.QtWidgets import (
    QWidget, QVBoxLayout, QHBoxLayout, QLabel, QFrame, QPushButton
)
from PySide6.QtCore import Qt, QUrl
from PySide6.QtWebSockets import QWebSocket
from client.src.components.code_editor import CodeEditor
from client.src.services.api_client import api
from client.src.components.toast import ToastNotification
from client.src.services.auth_service import auth

class ExerciseView(QWidget):
    def __init__(self, exercise_data=None, parent=None):
        super().__init__(parent)
        self.exercise = exercise_data or {}
        
        layout = QVBoxLayout(self)
        layout.setContentsMargins(28, 24, 28, 28)
        layout.setSpacing(20)

        # Header
        header = QLabel(self.exercise.get("title", "Exercițiu Nou"))
        header.setStyleSheet("color: #ffffff; font-size: 24px; font-weight: 800;")
        layout.addWidget(header)

        # Instructions
        instr = QLabel(self.exercise.get("description", "Scrie codul tău mai jos:"))
        instr.setStyleSheet("color: #94a3b8; font-size: 14px; margin-bottom: 10px;")
        instr.setWordWrap(True)
        layout.addWidget(instr)

        # Editor
        self.editor = CodeEditor()
        self.editor.setPlainText(self.exercise.get("starter_code", "# Scrie codul tău aici\n"))
        layout.addWidget(self.editor)

        # WebSocket Setup for Live Coding Feed
        self.socket = QWebSocket()
        user_id = auth.current_user.get("id") if auth.current_user else 0
        self.socket.open(QUrl(f"ws://127.0.0.1:8000/api/v1/notifications/ws/{user_id}"))
        self.editor.text_changed.connect(self.send_live_code)

        # Submit Button
        self.submit_btn = QPushButton("Trimite Soluția")
        self.submit_btn.setStyleSheet("""
            QPushButton {
                background-color: #10b981;
                color: white;
                font-weight: 700;
                padding: 12px;
                border-radius: 8px;
                border: none;
            }
            QPushButton:hover { background-color: #059669; }
        """)
        self.submit_btn.clicked.connect(self.submit_code)
        layout.addWidget(self.submit_btn)

        # Back Button
        self.back_btn = QPushButton("← Înapoi la Teme")
        self.back_btn.setStyleSheet("""
            QPushButton {
                background-color: transparent;
                color: #94a3b8;
                font-weight: 600;
                padding: 8px;
                border: 1px solid #374151;
                border-radius: 8px;
            }
            QPushButton:hover { background-color: #1f2937; color: white; }
        """)
        self.back_btn.clicked.connect(self.go_back)
        layout.addWidget(self.back_btn)

    def send_live_code(self, code):
        if self.socket.isValid():
            self.socket.sendTextMessage(code)

    def go_back(self):
        # Navigăm înapoi la Teme (Index 2 în main.py)
        if hasattr(self.window(), "views_stack"):
            self.window().views_stack.setCurrentIndex(2)
            self.window().header.set_title("Teme & Proiecte", "Monitorizarea temelor", "Teme")

    def submit_code(self):
        code = self.editor.toPlainText()
        
        try:
            # Apelăm endpoint-ul real de validare
            result = api.post("/exercises/validate", json_data={"code": code, "exercise_id": self.exercise.get("id")})
            
            if result.get("status") == "success":
                msg = f"✅ {result.get('message')}"
            else:
                msg = f"❌ {result.get('message')}"
            
            # Afișăm toast-ul
            toast = ToastNotification(msg, self)
            toast.show_toast(self.width() // 2 - 100, self.height() - 60)
                
        except Exception as e:
            toast = ToastNotification(f"❌ Eroare: {str(e)}", self)
            toast.show_toast(self.width() // 2 - 100, self.height() - 60)

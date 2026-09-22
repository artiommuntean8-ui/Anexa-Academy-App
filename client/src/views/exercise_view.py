from PySide6.QtWidgets import (
    QWidget, QVBoxLayout, QHBoxLayout, QLabel, QFrame, QPushButton
)
from PySide6.QtCore import Qt, QUrl
from PySide6.QtWebSockets import QWebSocket
import logging
from client.src.components.code_editor import CodeEditor
from client.src.components.toast import ToastManager
from client.src.services.api_client import api
from client.src.services.auth_service import auth

logger = logging.getLogger("client.exercise_view")

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
        try:
            self.socket.open(QUrl(f"ws://127.0.0.1:8000/api/v1/notifications/ws/{user_id}"))
            self.editor.text_changed.connect(self.send_live_code)
        except Exception as e:
            logger.error(f"WebSocket connection error: {e}")
            # Continue without WebSocket - it's optional

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

        # Use async API call to avoid UI blocking
        api.post("/exercises/validate",
                json_data={"code": code, "exercise_id": self.exercise.get("id")},
                callback=self._on_submit_success,
                error_callback=self._on_submit_error)

    def _on_submit_success(self, result):
        try:
            if result.get("status") == "success":
                msg = f"✅ {result.get('message', 'Soluție validată cu succes!')}"
                ToastManager.show_success(msg, parent=self)
            else:
                msg = f"❌ {result.get('message', 'Soluția nu a trecut testele.')}"
                ToastManager.show_error(msg, parent=self)
        except Exception as e:
            logger.error(f"Error processing submit result: {e}")
            ToastManager.show_error("Eroare la procesarea rezultatului", parent=self)

    def _on_submit_error(self, error_msg):
        logger.error(f"Submit code error: {error_msg}")
        ToastManager.show_error(f"Eroare la trimitere: {error_msg}", parent=self)

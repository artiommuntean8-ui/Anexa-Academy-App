from PySide6.QtWidgets import (
    QWidget, QVBoxLayout, QHBoxLayout, QLabel, QFrame, QPushButton
)
from PySide6.QtCore import Qt
from client.src.components.code_editor import CodeEditor
from client.src.services.api_client import api

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

        # Feedback Area
        self.feedback_lbl = QLabel("")
        self.feedback_lbl.setStyleSheet("color: #ffffff; font-size: 14px; font-weight: 600; padding: 10px;")
        layout.addWidget(self.feedback_lbl)

    def submit_code(self):
        code = self.editor.toPlainText()
        self.feedback_lbl.setText("Se verifică...")
        
        try:
            # Apelăm endpoint-ul real de validare
            result = api.post("/exercises/validate", json_data={"code": code, "exercise_id": self.exercise.get("id")})
            
            if result.get("status") == "success":
                self.feedback_lbl.setText(f"✅ {result.get('message')}")
                self.feedback_lbl.setStyleSheet("color: #34d399; background: rgba(16, 185, 129, 0.1); border-radius: 8px;")
            else:
                self.feedback_lbl.setText(f"❌ {result.get('message')}")
                self.feedback_lbl.setStyleSheet("color: #f87171; background: rgba(239, 68, 68, 0.1); border-radius: 8px;")
                
        except Exception as e:
            self.feedback_lbl.setText(f"❌ Eroare de conectare: {str(e)}")
            self.feedback_lbl.setStyleSheet("color: #f87171; background: rgba(239, 68, 68, 0.1); border-radius: 8px;")

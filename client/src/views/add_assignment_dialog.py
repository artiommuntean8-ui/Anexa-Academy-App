from PySide6.QtWidgets import (
    QDialog, QVBoxLayout, QHBoxLayout, QLineEdit, QTextEdit, QLabel, QPushButton, QMessageBox
)
from client.src.services.api_client import api


class AddAssignmentDialog(QDialog):
    """Dialog for instructors to create a new assignment/exercise."""

    def __init__(self, course_id: int = 1, parent=None):
        super().__init__(parent)
        self.course_id = course_id
        self.setWindowTitle("Adaugă Temă / Lecție Nouă")
        self.setMinimumWidth(460)
        self.setStyleSheet("""
            QDialog {
                background-color: #0f172a;
                color: #f8fafc;
            }
            QLabel {
                color: #94a3b8;
                font-weight: 700;
                font-size: 12px;
            }
            QLineEdit, QTextEdit {
                background-color: #1e293b;
                border: 1px solid rgba(255, 255, 255, 0.12);
                border-radius: 8px;
                padding: 10px;
                color: #ffffff;
            }
        """)

        layout = QVBoxLayout(self)
        layout.setContentsMargins(24, 24, 24, 24)
        layout.setSpacing(12)

        # Title
        layout.addWidget(QLabel("Titlu Temă / Proiect:"))
        self.title_input = QLineEdit()
        self.title_input.setPlaceholderText("ex: Exercițiu: Calculator simplu")
        layout.addWidget(self.title_input)

        # Description
        layout.addWidget(QLabel("Instrucțiuni & Descriere:"))
        self.desc_input = QTextEdit()
        self.desc_input.setPlaceholderText("Scrie cerințele exercițiului...")
        self.desc_input.setFixedHeight(80)
        layout.addWidget(self.desc_input)

        # Starter Code
        layout.addWidget(QLabel("Cod Starter Python (Opțional):"))
        self.code_input = QTextEdit()
        self.code_input.setPlaceholderText("# Scrie codul de pornire aici...\nprint('Salut, ArkiTech!')")
        self.code_input.setFixedHeight(100)
        layout.addWidget(self.code_input)

        # Buttons
        btn_layout = QHBoxLayout()
        btn_layout.setSpacing(10)

        cancel_btn = QPushButton("Anulează")
        cancel_btn.setStyleSheet("""
            QPushButton {
                background-color: #334155;
                color: #ffffff;
                border-radius: 8px;
                padding: 10px 16px;
                font-weight: 600;
            }
        """)
        cancel_btn.clicked.connect(self.reject)
        btn_layout.addWidget(cancel_btn)

        submit_btn = QPushButton("Creează Tema")
        submit_btn.setStyleSheet("""
            QPushButton {
                background-color: #4f46e5;
                color: #ffffff;
                border-radius: 8px;
                padding: 10px 16px;
                font-weight: 700;
            }
            QPushButton:hover {
                background-color: #4338ca;
            }
        """)
        submit_btn.clicked.connect(self.save_assignment)
        btn_layout.addWidget(submit_btn)

        layout.addLayout(btn_layout)

    def save_assignment(self):
        title = self.title_input.text().strip()
        if not title:
            QMessageBox.warning(self, "Atenție", "Vă rugăm să introduceți un titlu pentru temă.")
            return

        payload = {
            "title": title,
            "description": self.desc_input.toPlainText().strip(),
            "course_id": self.course_id,
            "max_score": 100.0
        }
        try:
            api.post("/assignments/", json_data=payload)
            QMessageBox.information(self, "Succes", "Tema a fost creată și adăugată în catalog!")
            self.accept()
        except Exception as e:
            QMessageBox.critical(self, "Eroare", f"Nu s-a putut salva tema: {str(e)}")

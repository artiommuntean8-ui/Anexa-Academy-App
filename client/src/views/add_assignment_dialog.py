from PySide6.QtWidgets import (
    QDialog, QVBoxLayout, QLineEdit, QTextEdit, QLabel, QPushButton, QMessageBox
)
from client.src.services.api_client import api

class AddAssignmentDialog(QDialog):
    def __init__(self, course_id=1, parent=None):
        super().__init__(parent)
        self.setWindowTitle("Adaugă Temă Nouă")
        self.setMinimumWidth(400)
        
        layout = QVBoxLayout(self)
        
        self.title_input = QLineEdit()
        self.title_input.setPlaceholderText("Titlu Temă")
        layout.addWidget(QLabel("Titlu:"))
        layout.addWidget(self.title_input)
        
        self.desc_input = QTextEdit()
        self.desc_input.setPlaceholderText("Descrierea exercițiului...")
        layout.addWidget(QLabel("Descriere:"))
        layout.addWidget(self.desc_input)
        
        self.code_input = QTextEdit()
        self.code_input.setPlaceholderText("# Scrie codul de pornire aici...")
        layout.addWidget(QLabel("Cod Starter:"))
        layout.addWidget(self.code_input)
        
        submit_btn = QPushButton("Salvează")
        submit_btn.clicked.connect(self.save_assignment)
        layout.addWidget(submit_btn)
        
        self.course_id = course_id

    def save_assignment(self):
        payload = {
            "title": self.title_input.text(),
            "description": self.desc_input.toPlainText(),
            "starter_code": self.code_input.toPlainText(),
            "course_id": self.course_id,
            "max_score": 100
        }
        try:
            api.post("/assignments/", json_data=payload)
            QMessageBox.information(self, "Succes", "Tema a fost adăugată!")
            self.accept()
        except Exception as e:
            QMessageBox.critical(self, "Eroare", str(e))

from PySide6.QtWidgets import QDialog, QVBoxLayout, QLineEdit, QTextEdit, QPushButton, QMessageBox
from client.src.services.api_client import api

class GradeDialog(QDialog):
    def __init__(self, grade_id, current_score, current_feedback, parent=None):
        super().__init__(parent)
        self.grade_id = grade_id
        self.setWindowTitle("Modifică Notă")
        
        layout = QVBoxLayout(self)
        
        self.score_input = QLineEdit()
        self.score_input.setText(str(current_score))
        layout.addWidget(QLabel("Notă:"))
        layout.addWidget(self.score_input)
        
        self.feedback_input = QTextEdit()
        self.feedback_input.setPlainText(current_feedback or "")
        layout.addWidget(QLabel("Feedback:"))
        layout.addWidget(self.feedback_input)
        
        btn = QPushButton("Salvează Nota")
        btn.clicked.connect(self.save)
        layout.addWidget(btn)
        
    def save(self):
        try:
            api.put(f"/grades/{self.grade_id}", json_data={
                "score": float(self.score_input.text()),
                "feedback": self.feedback_input.toPlainText()
            })
            self.accept()
        except Exception as e:
            QMessageBox.critical(self, "Eroare", str(e))

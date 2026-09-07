from PySide6.QtWidgets import QDialog, QVBoxLayout, QHBoxLayout, QLineEdit, QTextEdit, QPushButton, QMessageBox, QLabel
from PySide6.QtCore import Qt
from client.src.services.api_client import api


class GradeDialog(QDialog):
    """Dialog for updating a student's grade score and written feedback."""

    def __init__(self, grade_id: int, current_score: float, current_feedback: str = "", parent=None):
        super().__init__(parent)
        self.grade_id = grade_id
        self.setWindowTitle("Modificare Notă & Feedback")
        self.setMinimumWidth(420)
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
        layout.setSpacing(14)

        # Score input
        layout.addWidget(QLabel("Notă / Punctaj (0 - 100):"))
        self.score_input = QLineEdit()
        self.score_input.setText(str(current_score))
        layout.addWidget(self.score_input)

        # Feedback input
        layout.addWidget(QLabel("Feedback & Recomandări:"))
        self.feedback_input = QTextEdit()
        self.feedback_input.setPlainText(current_feedback or "")
        self.feedback_input.setFixedHeight(100)
        layout.addWidget(self.feedback_input)

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

        save_btn = QPushButton("Salvează Nota")
        save_btn.setStyleSheet("""
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
        save_btn.clicked.connect(self.save)
        btn_layout.addWidget(save_btn)

        layout.addLayout(btn_layout)

    def save(self):
        try:
            score = float(self.score_input.text().strip())
            feedback = self.feedback_input.toPlainText().strip()
            api.put(f"/grades/{self.grade_id}", json_data={
                "score": score,
                "feedback": feedback
            })
            self.accept()
        except ValueError:
            QMessageBox.warning(self, "Atenție", "Vă rugăm să introduceți un punctaj numeric valid.")
        except Exception as e:
            QMessageBox.critical(self, "Eroare", str(e))

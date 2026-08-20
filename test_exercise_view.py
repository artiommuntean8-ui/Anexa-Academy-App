from PySide6.QtWidgets import QApplication, QMainWindow, QVBoxLayout, QWidget
from client.src.views.exercise_view import ExerciseView
import sys

class TestExerciseWindow(QMainWindow):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("Test Exercise View")
        self.resize(800, 600)
        
        container = QWidget()
        layout = QVBoxLayout(container)
        
        # Date de test pentru exercițiu
        sample_exercise = {
            "title": "Exercițiul 1: Salutare",
            "description": "Scrie un program care afișează 'Salut, Python!' folosind funcția print.",
            "starter_code": "def salut():\n    # Scrie codul tău aici\n    pass"
        }
        
        self.exercise_view = ExerciseView(exercise_data=sample_exercise)
        layout.addWidget(self.exercise_view)
        
        self.setCentralWidget(container)

if __name__ == "__main__":
    app = QApplication(sys.argv)
    window = TestExerciseWindow()
    window.show()
    sys.exit(app.exec())

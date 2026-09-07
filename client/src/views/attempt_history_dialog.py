from PySide6.QtWidgets import QDialog, QVBoxLayout, QListWidget, QListWidgetItem, QLabel, QTextEdit
from client.src.services.api_client import api

class AttemptHistoryDialog(QDialog):
    def __init__(self, student_id, assignment_id, parent=None):
        super().__init__(parent)
        self.setWindowTitle("Istoric Încercări Elev")
        self.resize(600, 400)
        
        layout = QVBoxLayout(self)
        self.list_widget = QListWidget()
        layout.addWidget(self.list_widget)
        
        self.load_history(student_id, assignment_id)

    def load_history(self, student_id, assignment_id):
        try:
            history = api.get(f"/exercises/history/{student_id}/{assignment_id}")
            for entry in history:
                item = QListWidgetItem(f"{entry['timestamp']} - {entry['feedback']}")
                item.setData(Qt.UserRole, entry['code'])
                self.list_widget.addItem(item)
            self.list_widget.itemClicked.connect(self.show_code)
        except Exception as e:
            self.list_widget.addItem(f"Eroare: {str(e)}")

    def show_code(self, item):
        code = item.data(Qt.UserRole)
        # Putem deschide un mic dialog sau afișa într-un QTextEdit
        d = QDialog(self)
        d.setWindowTitle("Cod Trimis")
        layout = QVBoxLayout(d)
        edit = QTextEdit()
        edit.setPlainText(code)
        edit.setReadOnly(True)
        layout.addWidget(edit)
        d.exec()

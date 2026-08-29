from PySide6.QtWidgets import (
    QWidget, QVBoxLayout, QTableWidget, QTableWidgetItem, QHeaderView, QLabel, QFrame
)
from client.src.services.api_client import api

class StudentManagementView(QWidget):
    def __init__(self, parent=None):
        super().__init__(parent)
        layout = QVBoxLayout(self)
        
        header = QLabel("Management Elevi")
        header.setStyleSheet("color: white; font-size: 20px; font-weight: bold;")
        layout.addWidget(header)
        
        self.table = QTableWidget()
        self.table.setColumnCount(3)
        self.table.setHorizontalHeaderLabels(["Nume", "Cod Elev", "Email"])
        self.table.horizontalHeader().setSectionResizeMode(QHeaderView.Stretch)
        layout.addWidget(self.table)
        
        self.refresh_data()

    def refresh_data(self):
        try:
            students = api.get("/students/")
            self.table.setRowCount(len(students))
            for row, s in enumerate(students):
                self.table.setItem(row, 0, QTableWidgetItem(s.get("full_name", "")))
                self.table.setItem(row, 1, QTableWidgetItem(s.get("student_code", "")))
                self.table.setItem(row, 2, QTableWidgetItem(s.get("email", "")))
        except Exception as e:
            print(f"Error loading students: {e}")

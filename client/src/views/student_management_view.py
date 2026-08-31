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
        
        # Search Bar
        self.search_input = QLineEdit()
        self.search_input.setPlaceholderText("Caută elev...")
        self.search_input.textChanged.connect(self.filter_students)
        layout.addWidget(self.search_input)

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
    def filter_students(self, text):
        for i in range(self.table.rowCount()):
            item = self.table.item(i, 0)
            self.table.setRowHidden(i, text.lower() not in item.text().lower())

            for row, s in enumerate(students):
                self.table.setItem(row, 0, QTableWidgetItem(s.get("full_name", "")))
                self.table.setItem(row, 1, QTableWidgetItem(s.get("student_code", "")))
                self.table.setItem(row, 2, QTableWidgetItem(s.get("email", "")))
        except Exception as e:
            print(f"Error loading students: {e}")

from PySide6.QtWidgets import (
    QWidget, QVBoxLayout, QHBoxLayout, QTableWidget, QTableWidgetItem, QHeaderView, QLabel, QFrame, QLineEdit
)
from PySide6.QtCore import Qt
from client.src.components.badge import StatusBadge
from client.src.components.empty_state import EmptyState
from client.src.services.api_client import api


class StudentManagementView(QWidget):
    """Instructor view for monitoring enrolled students and academic performance."""

    def __init__(self, parent=None):
        super().__init__(parent)
        self.setObjectName("StudentManagementView")

        layout = QVBoxLayout(self)
        layout.setContentsMargins(28, 24, 28, 28)
        layout.setSpacing(20)

        # Header Info Card
        header_card = QFrame()
        header_card.setStyleSheet("""
            QFrame {
                background-color: #111827;
                border: 1px solid rgba(255, 255, 255, 0.08);
                border-radius: 14px;
                padding: 16px 20px;
            }
        """)
        hc_layout = QHBoxLayout(header_card)
        hc_layout.setContentsMargins(0, 0, 0, 0)

        info_vbox = QVBoxLayout()
        info_vbox.setSpacing(2)
        h_title = QLabel("Gestionare & Monitorizare Elevi")
        h_title.setStyleSheet("color: #ffffff; font-size: 18px; font-weight: 800;")
        h_sub = QLabel("Panou dedicat profesorilor pentru vizualizarea elevilor înscriși și a grupelor.")
        h_sub.setStyleSheet("color: #94a3b8; font-size: 12px;")
        info_vbox.addWidget(h_title)
        info_vbox.addWidget(h_sub)
        hc_layout.addLayout(info_vbox)
        hc_layout.addStretch()

        layout.addWidget(header_card)

        # Search Bar
        self.search_input = QLineEdit()
        self.search_input.setPlaceholderText("🔍 Caută după nume, cod elev sau email...")
        self.search_input.setStyleSheet("""
            QLineEdit {
                background-color: #111827;
                border: 1px solid rgba(255, 255, 255, 0.1);
                border-radius: 9px;
                padding: 10px 14px;
                color: #ffffff;
                font-size: 13px;
            }
            QLineEdit:focus {
                border-color: #6366f1;
            }
        """)
        self.search_input.textChanged.connect(self.filter_students)
        layout.addWidget(self.search_input)

        # Students Table
        self.table = QTableWidget()
        self.table.setColumnCount(4)
        self.table.setHorizontalHeaderLabels(["Nume Elev", "Cod Matricol", "Email Instituțional", "Departament / Grupă"])
        self.table.horizontalHeader().setSectionResizeMode(0, QHeaderView.Stretch)
        self.table.horizontalHeader().setSectionResizeMode(1, QHeaderView.ResizeToContents)
        self.table.horizontalHeader().setSectionResizeMode(2, QHeaderView.ResizeToContents)
        self.table.horizontalHeader().setSectionResizeMode(3, QHeaderView.ResizeToContents)
        self.table.verticalHeader().setVisible(False)
        self.table.setSelectionBehavior(QTableWidget.SelectRows)
        self.table.setEditTriggers(QTableWidget.NoEditTriggers)
        self.table.setStyleSheet("""
            QTableWidget {
                background-color: #111827;
                border: 1px solid rgba(255, 255, 255, 0.08);
                border-radius: 12px;
                color: #f1f5f9;
                gridline-color: rgba(255, 255, 255, 0.05);
            }
            QHeaderView::section {
                background-color: #0d1322;
                color: #94a3b8;
                padding: 14px 12px;
                border: none;
                border-bottom: 1px solid rgba(255, 255, 255, 0.08);
                font-weight: 700;
                font-size: 11px;
                text-transform: uppercase;
                letter-spacing: 0.5px;
            }
            QTableWidget::item {
                padding: 14px 10px;
                border-bottom: 1px solid rgba(255, 255, 255, 0.04);
            }
        """)
        layout.addWidget(self.table)

    def refresh_data(self):
        try:
            students = api.get("/students/")
            self.table.setRowCount(len(students))
            for row, s in enumerate(students):
                name_item = QTableWidgetItem(f"  👨‍🎓  {s.get('full_name', '')}")
                name_item.setTextAlignment(Qt.AlignVCenter | Qt.AlignLeft)
                self.table.setItem(row, 0, name_item)

                code_item = QTableWidgetItem(f" {s.get('student_code', '')} ")
                code_item.setTextAlignment(Qt.AlignCenter)
                self.table.setItem(row, 1, code_item)

                email_item = QTableWidgetItem(f" {s.get('email', '')} ")
                email_item.setTextAlignment(Qt.AlignCenter)
                self.table.setItem(row, 2, email_item)

                dept_item = QTableWidgetItem(f" {s.get('department', 'Nespecificat')} ")
                dept_item.setTextAlignment(Qt.AlignCenter)
                self.table.setItem(row, 3, dept_item)

                self.table.setRowHeight(row, 48)
        except Exception as e:
            print(f"Error loading students: {e}")

    def filter_students(self, text: str):
        text_lower = text.lower()
        for i in range(self.table.rowCount()):
            name_item = self.table.item(i, 0)
            code_item = self.table.item(i, 1)
            email_item = self.table.item(i, 2)
            
            match = False
            for it in [name_item, code_item, email_item]:
                if it and text_lower in it.text().lower():
                    match = True
                    break
            self.table.setRowHidden(i, not match)

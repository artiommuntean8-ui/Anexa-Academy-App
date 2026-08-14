from PySide6.QtWidgets import (
    QWidget, QVBoxLayout, QHBoxLayout, QLabel, QFrame, QScrollArea, QTableWidget, QTableWidgetItem, QHeaderView
)
from PySide6.QtCore import Qt
from client.src.services.api_client import api
from client.src.services.auth_service import auth


class AssignmentsView(QWidget):
    """Assignments and coursework management view."""

    def __init__(self, parent=None):
        super().__init__(parent)
        self.setObjectName("AssignmentsView")

        outer_layout = QVBoxLayout(self)
        outer_layout.setContentsMargins(0, 0, 0, 0)

        scroll = QScrollArea()
        scroll.setWidgetResizable(True)
        scroll.setStyleSheet("QScrollArea { border: none; background-color: #0b0f19; }")

        container = QWidget()
        container.setStyleSheet("background-color: #0b0f19;")
        self.layout = QVBoxLayout(container)
        self.layout.setContentsMargins(24, 20, 24, 24)
        self.layout.setSpacing(16)

        # Header
        h_title = QLabel("Teme & Proiecte de Curs")
        h_title.setStyleSheet("color: #ffffff; font-size: 18px; font-weight: 700;")
        self.layout.addWidget(h_title)

        # Assignments table
        self.table = QTableWidget()
        self.table.setColumnCount(4)
        self.table.setHorizontalHeaderLabels(["Titlu Temă / Proiect", "Curs ID", "Punctaj Maxim", "Termen Limită"])
        self.table.horizontalHeader().setSectionResizeMode(0, QHeaderView.Stretch)
        self.table.horizontalHeader().setSectionResizeMode(1, QHeaderView.ResizeToContents)
        self.table.horizontalHeader().setSectionResizeMode(2, QHeaderView.ResizeToContents)
        self.table.horizontalHeader().setSectionResizeMode(3, QHeaderView.ResizeToContents)
        self.table.verticalHeader().setVisible(False)
        self.table.setSelectionBehavior(QTableWidget.SelectRows)
        self.table.setEditTriggers(QTableWidget.NoEditTriggers)
        self.table.setStyleSheet("""
            QTableWidget {
                background-color: #131d33;
                border: 1px solid #1e293b;
                border-radius: 8px;
                color: #e2e8f0;
                gridline-color: #1e293b;
            }
            QHeaderView::section {
                background-color: #0f172a;
                color: #94a3b8;
                padding: 10px;
                border: none;
                border-bottom: 1px solid #1e293b;
                font-weight: 600;
            }
            QTableWidget::item {
                padding: 12px 8px;
            }
        """)

        self.layout.addWidget(self.table)
        scroll.setWidget(container)
        outer_layout.addWidget(scroll)

    def refresh_data(self):
        """Load assignments from backend."""
        try:
            assignments = api.get("/assignments/")
            self.table.setRowCount(len(assignments))

            for row, a in enumerate(assignments):
                title_item = QTableWidgetItem(a.get("title", ""))
                course_item = QTableWidgetItem(f"Curs #{a.get('course_id')}")
                score_item = QTableWidgetItem(f"{a.get('max_score', 100)}p")
                
                due = a.get("due_date", "")
                due_str = due[:10] if due else "Fără termen"
                due_item = QTableWidgetItem(due_str)

                title_item.setTextAlignment(Qt.AlignVCenter | Qt.AlignLeft)
                course_item.setTextAlignment(Qt.AlignCenter)
                score_item.setTextAlignment(Qt.AlignCenter)
                due_item.setTextAlignment(Qt.AlignCenter)

                self.table.setItem(row, 0, title_item)
                self.table.setItem(row, 1, course_item)
                self.table.setItem(row, 2, score_item)
                self.table.setItem(row, 3, due_item)
                self.table.setRowHeight(row, 44)
        except Exception as e:
            print(f"Error loading assignments: {e}")

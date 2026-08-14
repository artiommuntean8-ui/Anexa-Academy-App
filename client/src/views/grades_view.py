from PySide6.QtWidgets import (
    QWidget, QVBoxLayout, QHBoxLayout, QLabel, QFrame, QScrollArea, QTableWidget, QTableWidgetItem, QHeaderView
)
from PySide6.QtCore import Qt
from client.src.services.api_client import api
from client.src.services.auth_service import auth


class GradesView(QWidget):
    """Academic grades, performance, and feedback view."""

    def __init__(self, parent=None):
        super().__init__(parent)
        self.setObjectName("GradesView")

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

        # Header with GPA badge
        header_box = QHBoxLayout()
        h_title = QLabel("Note și Situație Academică")
        h_title.setStyleSheet("color: #ffffff; font-size: 18px; font-weight: 700;")
        header_box.addWidget(h_title)
        header_box.addStretch()

        self.gpa_badge = QLabel("Medie: 0.0 / 100")
        self.gpa_badge.setStyleSheet("""
            background-color: rgba(16, 185, 129, 0.15);
            color: #34d399;
            font-weight: 800;
            font-size: 13px;
            padding: 6px 14px;
            border-radius: 8px;
            border: 1px solid rgba(16, 185, 129, 0.3);
        """)
        header_box.addWidget(self.gpa_badge)
        self.layout.addLayout(header_box)

        # Grades Table
        self.table = QTableWidget()
        self.table.setColumnCount(4)
        self.table.setHorizontalHeaderLabels(["ID Temă", "Notă / Punctaj", "Feedback Instructor", "Data Notării"])
        self.table.horizontalHeader().setSectionResizeMode(0, QHeaderView.ResizeToContents)
        self.table.horizontalHeader().setSectionResizeMode(1, QHeaderView.ResizeToContents)
        self.table.horizontalHeader().setSectionResizeMode(2, QHeaderView.Stretch)
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
        """Fetch grades from backend."""
        user = auth.current_user
        if not user:
            return

        student_id = user.get("id")
        try:
            grades = api.get("/grades/", params={"student_id": student_id})
            self.table.setRowCount(len(grades))

            total_score = 0.0
            for row, g in enumerate(grades):
                score = g.get("score", 0.0)
                total_score += score

                a_item = QTableWidgetItem(f"Temă #{g.get('assignment_id')}")
                s_item = QTableWidgetItem(f"{score:.1f}p")
                f_item = QTableWidgetItem(g.get("feedback") or "Fără observații suplimentare")
                
                d = g.get("graded_at", "")
                d_str = d[:10] if d else "-"
                d_item = QTableWidgetItem(d_str)

                a_item.setTextAlignment(Qt.AlignCenter)
                s_item.setTextAlignment(Qt.AlignCenter)
                f_item.setTextAlignment(Qt.AlignVCenter | Qt.AlignLeft)
                d_item.setTextAlignment(Qt.AlignCenter)

                self.table.setItem(row, 0, a_item)
                self.table.setItem(row, 1, s_item)
                self.table.setItem(row, 2, f_item)
                self.table.setItem(row, 3, d_item)
                self.table.setRowHeight(row, 44)

            if grades:
                avg = total_score / len(grades)
                self.gpa_badge.setText(f"Medie Generală: {avg:.1f} / 100")
            else:
                self.gpa_badge.setText("Medie: -")

        except Exception as e:
            print(f"Error loading grades: {e}")

from typing import List
from PySide6.QtWidgets import (
    QWidget, QVBoxLayout, QHBoxLayout, QLabel, QFrame, QScrollArea, QPushButton, QTableWidget, QTableWidgetItem, QHeaderView
)
from PySide6.QtCore import Qt
from PySide6.QtGui import QCursor
from client.src.components.badge import StatusBadge
from client.src.components.empty_state import EmptyState
from client.src.services.api_client import api
from client.src.services.auth_service import auth


class AssignmentsView(QWidget):
    """Assignments view with filter tabs, status badges, and details ledger."""

    def __init__(self, parent=None):
        super().__init__(parent)
        self.setObjectName("AssignmentsView")

        self.all_assignments: List[dict] = []
        self.student_grades: dict = {}  # assignment_id -> grade_data

        outer_layout = QVBoxLayout(self)
        outer_layout.setContentsMargins(0, 0, 0, 0)

        scroll = QScrollArea()
        scroll.setWidgetResizable(True)
        scroll.setStyleSheet("QScrollArea { border: none; background-color: #090d16; }")

        container = QWidget()
        container.setStyleSheet("background-color: #090d16;")
        self.layout = QVBoxLayout(container)
        self.layout.setContentsMargins(28, 24, 28, 28)
        self.layout.setSpacing(20)

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

        # Buton pentru Profesor (dacă e cazul)
        if auth.current_user and auth.current_user.get("role") == "instructor":
            add_btn = QPushButton("＋ Adaugă Temă")
            add_btn.setStyleSheet("""
                QPushButton {
                    background-color: #3b82f6;
                    color: white;
                    font-weight: 700;
                    padding: 8px 16px;
                    border-radius: 8px;
                }
                QPushButton:hover { background-color: #2563eb; }
            """)
            hc_layout.addWidget(add_btn)

        info_vbox = QVBoxLayout()
        info_vbox.setSpacing(2)
        h_title = QLabel("Teme de Laborator & Proiecte")
        h_title.setStyleSheet("color: #ffffff; font-size: 17px; font-weight: 800;")
        h_sub = QLabel("Monitorizează starea temelor, cerințele și punctajul acordat.")
        h_sub.setStyleSheet("color: #94a3b8; font-size: 12px;")
        info_vbox.addWidget(h_title)
        info_vbox.addWidget(h_sub)
        hc_layout.addLayout(info_vbox)
        hc_layout.addStretch()

        self.layout.addWidget(header_card)

        # Assignments Table / Ledger
        self.table = QTableWidget()
        self.table.setColumnCount(5)
        self.table.setHorizontalHeaderLabels([
            "Titlu Temă / Proiect", "Curs Asociat", "Punctaj Maxim", "Termen Limită", "Stare Temă"
        ])
        self.table.horizontalHeader().setSectionResizeMode(0, QHeaderView.Stretch)
        self.table.horizontalHeader().setSectionResizeMode(1, QHeaderView.ResizeToContents)
        self.table.horizontalHeader().setSectionResizeMode(2, QHeaderView.ResizeToContents)
        self.table.horizontalHeader().setSectionResizeMode(3, QHeaderView.ResizeToContents)
        self.table.horizontalHeader().setSectionResizeMode(4, QHeaderView.ResizeToContents)
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

        self.layout.addWidget(self.table)
        scroll.setWidget(container)
        outer_layout.addWidget(scroll)

    def refresh_data(self):
        """Load assignments and student grades."""
        user = auth.current_user
        if not user:
            return

        student_id = user.get("id")
        try:
            self.all_assignments = api.get("/assignments/")
            grades_list = api.get("/grades/", params={"student_id": student_id})
            self.student_grades = {g["assignment_id"]: g for g in grades_list}
            self._render_table()
        except Exception as e:
            print(f"Error loading assignments: {e}")

    def _render_table(self):
        self.table.setRowCount(len(self.all_assignments))
        self.table.cellClicked.connect(self._on_cell_clicked)

        for row, a in enumerate(self.all_assignments):
            a_id = a.get("id")
            grade_info = self.student_grades.get(a_id)

            # ... (restul codului de randare rămâne la fel)
            title_text = a.get("title", "")
            title_item = QTableWidgetItem(f"  📝  {title_text}")
            title_item.setTextAlignment(Qt.AlignVCenter | Qt.AlignLeft)
            self.table.setItem(row, 0, title_item)

            # 2. Course ID
            course_item = QTableWidgetItem(f" Curs #{a.get('course_id')} ")
            course_item.setTextAlignment(Qt.AlignCenter)
            self.table.setItem(row, 1, course_item)

            # 3. Max Score
            score_item = QTableWidgetItem(f" {a.get('max_score', 100):.0f} pct ")
            score_item.setTextAlignment(Qt.AlignCenter)
            self.table.setItem(row, 2, score_item)

            # 4. Due Date
            due = a.get("due_date", "")
            due_str = due[:10] if due else "Fără termen"
            due_item = QTableWidgetItem(f" 📅 {due_str} ")
            due_item.setTextAlignment(Qt.AlignCenter)
            self.table.setItem(row, 3, due_item)

            # 5. Status Badge Cell Widget
            cell_widget = QWidget()
            cell_layout = QHBoxLayout(cell_widget)
            cell_layout.setContentsMargins(8, 6, 8, 6)
            cell_layout.setAlignment(Qt.AlignCenter)

            if grade_info:
                score = grade_info.get("score", 0.0)
                badge = StatusBadge("graded", f"★ Notat ({score:.1f}p)")
            else:
                badge = StatusBadge("pending", "⏳ În Așteptare")

            cell_layout.addWidget(badge)
            self.table.setCellWidget(row, 4, cell_widget)
            self.table.setRowHeight(row, 50)

    def _on_cell_clicked(self, row, column):
        assignment = self.all_assignments[row]
        
        # Pregătim datele pentru ExerciseView
        exercise_data = {
            "id": assignment.get("id"),
            "title": assignment.get("title"),
            "description": assignment.get("description", "Exercițiu de programare Python"),
            "starter_code": assignment.get("starter_code", "# Scrie codul tău aici\n")
        }
        
        # Navigăm către ExerciseView folosind MainWindow
        if hasattr(self.window(), "show_exercise"):
            self.window().show_exercise(exercise_data)

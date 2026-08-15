from typing import List, Set
from PySide6.QtWidgets import (
    QWidget, QVBoxLayout, QHBoxLayout, QLabel, QFrame, QScrollArea, QPushButton, QLineEdit, QMessageBox
)
from PySide6.QtCore import Qt
from PySide6.QtGui import QCursor
from client.src.components.badge import StatusBadge
from client.src.components.empty_state import EmptyState
from client.src.services.api_client import api
from client.src.services.auth_service import auth


class CoursesView(QWidget):
    """Catalog of all academic courses with search, filtering, and enrollment management."""

    def __init__(self, parent=None):
        super().__init__(parent)
        self.setObjectName("CoursesView")

        self.all_courses: List[dict] = []
        self.enrolled_ids: Set[int] = set()
        self.active_filter = "all"  # "all", "enrolled", "available"

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

        # 1. Search & Filter Bar
        bar_frame = QFrame()
        bar_frame.setStyleSheet("""
            QFrame {
                background-color: #111827;
                border: 1px solid rgba(255, 255, 255, 0.08);
                border-radius: 12px;
                padding: 12px 16px;
            }
        """)
        bar_layout = QHBoxLayout(bar_frame)
        bar_layout.setContentsMargins(0, 0, 0, 0)
        bar_layout.setSpacing(12)

        # Search Input
        self.search_input = QLineEdit()
        self.search_input.setPlaceholderText("🔍 Caută după titlu, cod curs sau profesor...")
        self.search_input.setStyleSheet("""
            QLineEdit {
                background-color: #162035;
                border: 1px solid rgba(255, 255, 255, 0.1);
                border-radius: 8px;
                padding: 8px 12px;
                color: #ffffff;
                font-size: 13px;
            }
            QLineEdit:focus {
                border-color: #6366f1;
            }
        """)
        self.search_input.textChanged.connect(self._apply_filters)
        bar_layout.addWidget(self.search_input, stretch=2)

        # Filter buttons
        filter_layout = QHBoxLayout()
        filter_layout.setSpacing(8)

        self.btn_all = QPushButton("Toate Cursurile")
        self.btn_enrolled = QPushButton("Cursurile Mele")
        self.btn_available = QPushButton("Disponibile")

        self.filter_buttons = [
            (self.btn_all, "all"),
            (self.btn_enrolled, "enrolled"),
            (self.btn_available, "available")
        ]

        for btn, key in self.filter_buttons:
            btn.setCursor(QCursor(Qt.PointingHandCursor))
            btn.clicked.connect(lambda _, k=key: self._set_filter(k))
            filter_layout.addWidget(btn)

        self._update_filter_button_styles()
        bar_layout.addLayout(filter_layout)
        self.layout.addWidget(bar_frame)

        # 2. Courses List Container
        self.courses_container = QVBoxLayout()
        self.courses_container.setSpacing(14)
        self.layout.addLayout(self.courses_container)
        self.layout.addStretch()

        scroll.setWidget(container)
        outer_layout.addWidget(scroll)

    def _set_filter(self, filter_key: str):
        self.active_filter = filter_key
        self._update_filter_button_styles()
        self._apply_filters()

    def _update_filter_button_styles(self):
        active_style = """
            QPushButton {
                background-color: #4f46e5;
                color: #ffffff;
                border: 1px solid #6366f1;
                border-radius: 8px;
                padding: 8px 14px;
                font-size: 12px;
                font-weight: 700;
            }
        """
        inactive_style = """
            QPushButton {
                background-color: #1e293b;
                color: #94a3b8;
                border: 1px solid rgba(255, 255, 255, 0.08);
                border-radius: 8px;
                padding: 8px 14px;
                font-size: 12px;
                font-weight: 600;
            }
            QPushButton:hover {
                background-color: #334155;
                color: #ffffff;
            }
        """
        for btn, key in self.filter_buttons:
            btn.setStyleSheet(active_style if key == self.active_filter else inactive_style)

    def refresh_data(self):
        """Fetch all courses and student enrollments from backend."""
        user = auth.current_user
        if not user:
            return

        student_id = user.get("id")
        try:
            self.all_courses = api.get("/courses/")
            dash = api.get(f"/students/{student_id}/dashboard")
            self.enrolled_ids = {c["id"] for c in dash.get("enrolled_courses", [])}
            self._apply_filters()
        except Exception as e:
            print(f"Error loading courses: {e}")

    def _apply_filters(self):
        query = self.search_input.text().strip().lower()
        filtered = []

        for c in self.all_courses:
            c_id = c.get("id")
            is_enrolled = c_id in self.enrolled_ids

            # Filter tab logic
            if self.active_filter == "enrolled" and not is_enrolled:
                continue
            if self.active_filter == "available" and is_enrolled:
                continue

            # Search query logic
            title = c.get("title", "").lower()
            code = c.get("code", "").lower()
            instr = c.get("instructor_name", "").lower()

            if query and not (query in title or query in code or query in instr):
                continue

            filtered.append(c)

        user = auth.current_user
        student_id = user.get("id") if user else 1
        self._render_courses(filtered, student_id)

    def _render_courses(self, courses: list, student_id: int):
        while self.courses_container.count():
            item = self.courses_container.takeAt(0)
            if item.widget():
                item.widget().deleteLater()

        if not courses:
            empty = EmptyState(
                icon="🔍",
                title="Nu a fost găsit niciun curs",
                message="Încearcă să schimbi termenul de căutare sau filtrul activ."
            )
            self.courses_container.addWidget(empty)
            return

        for c in courses:
            c_id = c.get("id")
            is_enrolled = c_id in self.enrolled_ids

            card = QFrame()
            card.setStyleSheet("""
                QFrame {
                    background-color: #111827;
                    border: 1px solid rgba(255, 255, 255, 0.08);
                    border-radius: 14px;
                    padding: 20px;
                }
                QFrame:hover {
                    border: 1px solid rgba(99, 102, 241, 0.4);
                    background-color: #131c2e;
                }
            """)
            c_layout = QVBoxLayout(card)
            c_layout.setSpacing(12)

            # Top Header Row: Code + Title + Status Action
            top_bar = QHBoxLayout()
            top_bar.setSpacing(12)

            code_badge = QLabel(c.get("code", "CURS"))
            code_badge.setStyleSheet("""
                background-color: rgba(99, 102, 241, 0.15);
                color: #a5b4fc;
                font-weight: 800;
                font-size: 11px;
                padding: 4px 10px;
                border-radius: 6px;
                border: 1px solid rgba(99, 102, 241, 0.3);
            """)
            top_bar.addWidget(code_badge)

            title_lbl = QLabel(c.get("title", ""))
            title_lbl.setStyleSheet("color: #ffffff; font-size: 17px; font-weight: 800; letter-spacing: -0.2px;")
            top_bar.addWidget(title_lbl)
            top_bar.addStretch()

            if is_enrolled:
                enrolled_badge = StatusBadge("approved", "✓ Înscris la Curs")
                top_bar.addWidget(enrolled_badge)
            else:
                enroll_btn = QPushButton("Înscriere Curs")
                enroll_btn.setCursor(QCursor(Qt.PointingHandCursor))
                enroll_btn.setStyleSheet("""
                    QPushButton {
                        background-color: #4f46e5;
                        color: #ffffff;
                        border: 1px solid #6366f1;
                        border-radius: 8px;
                        padding: 7px 16px;
                        font-weight: 700;
                        font-size: 12px;
                    }
                    QPushButton:hover {
                        background-color: #4338ca;
                    }
                """)
                enroll_btn.clicked.connect(lambda _, cid=c_id: self._enroll_course(cid, student_id))
                top_bar.addWidget(enroll_btn)

            c_layout.addLayout(top_bar)

            # Meta Row: Instructor, ECTS, Semester
            meta_layout = QHBoxLayout()
            meta_layout.setSpacing(24)

            instr = QLabel(f"👨‍🏫 {c.get('instructor_name', 'Instructor ArkiTech')}")
            instr.setStyleSheet("color: #94a3b8; font-size: 12px; font-weight: 500;")
            meta_layout.addWidget(instr)

            credits = QLabel(f"🎖️ {c.get('credits', 5)} Credite ECTS")
            credits.setStyleSheet("color: #06b6d4; font-size: 12px; font-weight: 700;")
            meta_layout.addWidget(credits)

            sem = QLabel(f"📅 Semestrul {c.get('semester', 1)}")
            sem.setStyleSheet("color: #94a3b8; font-size: 12px;")
            meta_layout.addWidget(sem)
            meta_layout.addStretch()

            c_layout.addLayout(meta_layout)

            # Description
            if c.get("description"):
                desc = QLabel(c.get("description"))
                desc.setWordWrap(True)
                desc.setStyleSheet("color: #64748b; font-size: 12px; line-height: 1.4;")
                c_layout.addWidget(desc)

            self.courses_container.addWidget(card)

    def _enroll_course(self, course_id: int, student_id: int):
        try:
            api.post(
                f"/courses/{course_id}/enroll",
                json_data={"student_id": student_id, "course_id": course_id, "status": "active"}
            )
            QMessageBox.information(self, "Înscriere Reușită", "V-ați înscris cu succes la acest curs!")
            self.refresh_data()
        except Exception as e:
            QMessageBox.warning(self, "Eroare", f"Nu s-a putut efectua înscrierea: {str(e)}")

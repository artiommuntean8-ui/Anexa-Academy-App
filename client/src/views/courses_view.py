from PySide6.QtWidgets import (
    QWidget, QVBoxLayout, QHBoxLayout, QLabel, QFrame, QScrollArea, QPushButton, QMessageBox
)
from PySide6.QtCore import Qt
from PySide6.QtGui import QCursor
from client.src.services.api_client import api
from client.src.services.auth_service import auth


class CoursesView(QWidget):
    """Catalog of all academic courses with enrollment options."""

    def __init__(self, parent=None):
        super().__init__(parent)
        self.setObjectName("CoursesView")

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

        # Header info
        header_box = QHBoxLayout()
        h_title = QLabel("Catalog Cursuri Universitare")
        h_title.setStyleSheet("color: #ffffff; font-size: 18px; font-weight: 700;")
        header_box.addWidget(h_title)
        header_box.addStretch()
        self.layout.addLayout(header_box)

        # Courses list container
        self.courses_container = QVBoxLayout()
        self.courses_container.setSpacing(14)
        self.layout.addLayout(self.courses_container)
        self.layout.addStretch()

        scroll.setWidget(container)
        outer_layout.addWidget(scroll)

    def refresh_data(self):
        """Fetch all courses and enrollment status."""
        user = auth.current_user
        if not user:
            return

        student_id = user.get("id")
        try:
            all_courses = api.get("/courses/")
            # Get enrolled courses
            dash = api.get(f"/students/{student_id}/dashboard")
            enrolled_ids = {c["id"] for c in dash.get("enrolled_courses", [])}
            self._render_courses(all_courses, enrolled_ids, student_id)
        except Exception as e:
            print(f"Error loading courses: {e}")

    def _render_courses(self, courses: list, enrolled_ids: set, student_id: int):
        while self.courses_container.count():
            item = self.courses_container.takeAt(0)
            if item.widget():
                item.widget().deleteLater()

        if not courses:
            empty_lbl = QLabel("Nu există cursuri în catalog în acest moment.")
            empty_lbl.setStyleSheet("color: #64748b; padding: 20px;")
            self.courses_container.addWidget(empty_lbl)
            return

        for c in courses:
            c_id = c.get("id")
            is_enrolled = c_id in enrolled_ids

            card = QFrame()
            card.setStyleSheet("""
                QFrame {
                    background-color: #131d33;
                    border: 1px solid #1e293b;
                    border-radius: 12px;
                    padding: 18px;
                }
                QFrame:hover {
                    border-color: #334155;
                }
            """)
            c_layout = QVBoxLayout(card)
            c_layout.setSpacing(10)

            # Top bar
            top_bar = QHBoxLayout()
            code_badge = QLabel(c.get("code", ""))
            code_badge.setStyleSheet("background-color: rgba(59, 130, 246, 0.15); color: #60a5fa; font-weight: 700; font-size: 11px; padding: 4px 8px; border-radius: 6px;")
            top_bar.addWidget(code_badge)

            title_lbl = QLabel(c.get("title", ""))
            title_lbl.setStyleSheet("color: #ffffff; font-size: 16px; font-weight: 700;")
            top_bar.addWidget(title_lbl)
            top_bar.addStretch()

            if is_enrolled:
                enrolled_badge = QLabel("✓ Înscris la Curs")
                enrolled_badge.setStyleSheet("background-color: rgba(16, 185, 129, 0.15); color: #34d399; font-weight: 700; font-size: 11px; padding: 4px 10px; border-radius: 6px;")
                top_bar.addWidget(enrolled_badge)
            else:
                enroll_btn = QPushButton("Înscriere Curs")
                enroll_btn.setCursor(QCursor(Qt.PointingHandCursor))
                enroll_btn.setStyleSheet("""
                    QPushButton {
                        background-color: #2563eb;
                        color: #ffffff;
                        border: none;
                        border-radius: 6px;
                        padding: 6px 14px;
                        font-weight: 600;
                        font-size: 12px;
                    }
                    QPushButton:hover {
                        background-color: #1d4ed8;
                    }
                """)
                enroll_btn.clicked.connect(lambda _, cid=c_id: self._enroll_course(cid, student_id))
                top_bar.addWidget(enroll_btn)

            c_layout.addLayout(top_bar)

            # Meta details
            meta_layout = QHBoxLayout()
            meta_layout.setSpacing(20)

            instr = QLabel(f"👨‍🏫 Instructor: {c.get('instructor_name', 'Nespecificat')}")
            instr.setStyleSheet("color: #94a3b8; font-size: 12px;")
            meta_layout.addWidget(instr)

            credits = QLabel(f"🎖️ Credite: {c.get('credits', 5)} ECTS")
            credits.setStyleSheet("color: #94a3b8; font-size: 12px;")
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
                desc.setStyleSheet("color: #64748b; font-size: 12px;")
                c_layout.addWidget(desc)

            self.courses_container.addWidget(card)

    def _enroll_course(self, course_id: int, student_id: int):
        try:
            api.post(f"/courses/{course_id}/enroll", json_data={"student_id": student_id, "course_id": course_id, "status": "active"})
            QMessageBox.information(self, "Succes", "V-ați înscris cu succes la acest curs!")
            self.refresh_data()
        except Exception as e:
            QMessageBox.warning(self, "Eroare", f"Nu s-a putut efectua înscrierea: {str(e)}")

from PySide6.QtWidgets import (
    QWidget, QVBoxLayout, QHBoxLayout, QLabel, QFrame, QScrollArea, QPushButton
)
from PySide6.QtCore import Qt
from PySide6.QtGui import QCursor
from client.src.components.stat_card import StatCard
from client.src.components.progress_card import ProgressCard
from client.src.components.badge import StatusBadge
from client.src.components.empty_state import EmptyState
from client.src.services.api_client import api
from client.src.services.auth_service import auth


class DashboardView(QWidget):
    """Main overview dashboard with student KPIs, academic progress bar, active courses, and upcoming assignments."""

    def __init__(self, parent=None):
        super().__init__(parent)
        self.setObjectName("DashboardView")

        outer_layout = QVBoxLayout(self)
        outer_layout.setContentsMargins(0, 0, 0, 0)

        scroll = QScrollArea()
        scroll.setWidgetResizable(True)
        scroll.setStyleSheet("QScrollArea { border: none; background-color: #090d16; }")

        container = QWidget()
        container.setStyleSheet("background-color: #090d16;")
        self.layout = QVBoxLayout(container)
        self.layout.setContentsMargins(28, 24, 28, 28)
        self.layout.setSpacing(24)

        # 1. Error banner (Hidden by default)
        self.error_banner = QFrame()
        self.error_banner.setStyleSheet("""
            QFrame {
                background-color: rgba(239, 68, 68, 0.15);
                border: 1px solid rgba(239, 68, 68, 0.35);
                border-radius: 10px;
                padding: 12px 16px;
            }
        """)
        eb_layout = QHBoxLayout(self.error_banner)
        eb_layout.setContentsMargins(0, 0, 0, 0)
        self.error_msg_lbl = QLabel("Eroare de conexiune la server.")
        self.error_msg_lbl.setStyleSheet("color: #fca5a5; font-size: 12px; font-weight: 600;")
        eb_layout.addWidget(self.error_msg_lbl)
        eb_layout.addStretch()
        retry_btn = QPushButton("Reîncearcă")
        retry_btn.setCursor(QCursor(Qt.PointingHandCursor))
        retry_btn.setStyleSheet("""
            QPushButton {
                background-color: #ef4444;
                color: #ffffff;
                border: none;
                border-radius: 6px;
                padding: 5px 12px;
                font-size: 11px;
                font-weight: 700;
            }
            QPushButton:hover {
                background-color: #dc2626;
            }
        """)
        retry_btn.clicked.connect(self.refresh_data)
        eb_layout.addWidget(retry_btn)
        self.error_banner.hide()
        self.layout.addWidget(self.error_banner)

        # 2. Hero Welcome Banner
        self.welcome_banner = QFrame()
        self.welcome_banner.setStyleSheet("""
            QFrame {
                background: qlineargradient(x1:0, y1:0, x2:1, y2:0, stop:0 #1e1b4b, stop:0.5 #172554, stop:1 #0f172a);
                border: 1px solid rgba(99, 102, 241, 0.3);
                border-radius: 16px;
                padding: 20px 24px;
            }
        """)
        wb_layout = QHBoxLayout(self.welcome_banner)
        wb_layout.setContentsMargins(4, 4, 4, 4)

        wb_text_layout = QVBoxLayout()
        wb_text_layout.setSpacing(4)

        greeting_row = QHBoxLayout()
        greeting_row.setSpacing(8)
        self.wb_title = QLabel("Bine ai revenit, Student!")
        self.wb_title.setStyleSheet("color: #ffffff; font-size: 20px; font-weight: 800; letter-spacing: -0.3px;")
        greeting_row.addWidget(self.wb_title)

        self.student_badge = StatusBadge("enrolled", "Înmatriculat")
        greeting_row.addWidget(self.student_badge)
        greeting_row.addStretch()
        wb_text_layout.addLayout(greeting_row)

        self.wb_sub = QLabel("Panoul tău academic este sincronizat cu serverul ArkiTech.")
        self.wb_sub.setStyleSheet("color: #a5b4fc; font-size: 13px; font-weight: 500;")
        wb_text_layout.addWidget(self.wb_sub)

        wb_layout.addLayout(wb_text_layout)
        wb_layout.addStretch()

        hero_icon = QLabel("🎓")
        hero_icon.setStyleSheet("font-size: 38px; padding-right: 12px;")
        wb_layout.addWidget(hero_icon)

        self.layout.addWidget(self.welcome_banner)

        # 3. KPI Stat Cards Row
        stats_layout = QHBoxLayout()
        stats_layout.setSpacing(16)

        self.card_courses = StatCard("Cursuri Înscrise", "0", "📚", "#6366f1", "rgba(99, 102, 241, 0.12)", "Semestrul curent")
        self.card_credits = StatCard("Credite ECTS", "0", "🎖️", "#06b6d4", "rgba(6, 182, 212, 0.12)", "Total acumulat")
        self.card_gpa = StatCard("Medie Generală", "0.0", "⭐", "#10b981", "rgba(16, 185, 129, 0.12)", "Scala 0 - 100")
        self.card_assignments = StatCard("Teme Active", "0", "📝", "#f59e0b", "rgba(245, 158, 11, 0.12)", "În așteptare")

        stats_layout.addWidget(self.card_courses)
        stats_layout.addWidget(self.card_credits)
        stats_layout.addWidget(self.card_gpa)
        stats_layout.addWidget(self.card_assignments)

        self.layout.addLayout(stats_layout)

        # 4. Academic Progress Card (Custom visual progress bar)
        self.progress_card = ProgressCard()
        self.layout.addWidget(self.progress_card)

        # 5. Two Columns: Left (Enrolled Courses Grid) & Right (Upcoming Tasks & Recent Grades)
        main_content = QHBoxLayout()
        main_content.setSpacing(24)

        # Left Column: Cursurile Mele Active
        left_col = QVBoxLayout()
        left_col.setSpacing(12)

        left_header = QLabel("Cursurile Mele Active")
        left_header.setStyleSheet("color: #ffffff; font-size: 16px; font-weight: 700; letter-spacing: -0.2px;")
        left_col.addWidget(left_header)

        self.courses_container = QVBoxLayout()
        self.courses_container.setSpacing(12)
        left_col.addLayout(self.courses_container)
        left_col.addStretch()

        main_content.addLayout(left_col, stretch=3)

        # Right Column: Teme & Note Recente
        right_col = QVBoxLayout()
        right_col.setSpacing(20)

        # Assignments block
        assign_block = QVBoxLayout()
        assign_block.setSpacing(10)
        assign_header = QLabel("Teme & Termene de Predare")
        assign_header.setStyleSheet("color: #ffffff; font-size: 15px; font-weight: 700;")
        assign_block.addWidget(assign_header)

        self.assignments_container = QVBoxLayout()
        self.assignments_container.setSpacing(10)
        assign_block.addLayout(self.assignments_container)
        right_col.addLayout(assign_block)

        # Recent grades block
        grades_block = QVBoxLayout()
        grades_block.setSpacing(10)
        grades_header = QLabel("Ultimele Evaluări Primite")
        grades_header.setStyleSheet("color: #ffffff; font-size: 15px; font-weight: 700;")
        grades_block.addWidget(grades_header)

        self.grades_container = QVBoxLayout()
        self.grades_container.setSpacing(10)
        grades_block.addLayout(self.grades_container)
        right_col.addLayout(grades_block)

        right_col.addStretch()
        main_content.addLayout(right_col, stretch=2)

        self.layout.addLayout(main_content)

        scroll.setWidget(container)
        outer_layout.addWidget(scroll)

    def refresh_data(self):
        """Fetch latest dashboard stats from backend."""
        user = auth.current_user
        if not user:
            return

        student_id = user.get("id")
        self.wb_title.setText(f"Bine ai revenit, {user.get('full_name', 'Student')}!")
        self.wb_sub.setText(f"Departament: {user.get('department', 'Inginerie Software')} • Semestrul {user.get('semester', 1)}")

        try:
            self.error_banner.hide()
            data = api.get(f"/students/{student_id}/dashboard")
            self._update_kpis(data)
            self._render_courses(data.get("enrolled_courses", []))
            self._render_assignments(data.get("upcoming_assignments", []))
            self._render_grades(data.get("recent_grades", []))
        except Exception as e:
            self.error_msg_lbl.setText(f"Eroare la actualizarea datelor: {str(e)}")
            self.error_banner.show()

    def _update_kpis(self, data: dict):
        enrolled_courses_count = data.get("total_enrolled_courses", 0)
        total_credits = data.get("total_credits", 0)
        gpa = data.get("average_grade", 0.0)
        upcoming_count = len(data.get("upcoming_assignments", []))

        self.card_courses.set_value(str(enrolled_courses_count))
        self.card_credits.set_value(f"{total_credits} ECTS")
        self.card_gpa.set_value(f"{gpa:.1f}")
        self.card_assignments.set_value(str(upcoming_count))

        # Update progress bar
        self.progress_card.set_progress(current_credits=total_credits, total_target_credits=30, gpa=gpa)

    def _render_courses(self, courses: list):
        while self.courses_container.count():
            item = self.courses_container.takeAt(0)
            if item.widget():
                item.widget().deleteLater()

        if not courses:
            empty = EmptyState(
                icon="📚",
                title="Niciun curs înscris",
                message="Nu ești înscris la niciun curs în acest semestru. Accesează secțiunea Cursuri pentru a te înscrie."
            )
            self.courses_container.addWidget(empty)
            return

        for c in courses:
            card = QFrame()
            card.setObjectName("CourseItemCard")
            card.setStyleSheet("""
                QFrame#CourseItemCard {
                    background-color: #111827;
                    border: 1px solid rgba(255, 255, 255, 0.08);
                    border-radius: 14px;
                    padding: 16px;
                }
                QFrame#CourseItemCard:hover {
                    border: 1px solid rgba(99, 102, 241, 0.5);
                    background-color: #131c2e;
                }
            """)
            c_layout = QVBoxLayout(card)
            c_layout.setSpacing(8)

            # Top header row: Code Pill + Status Badge + Credits
            top = QHBoxLayout()
            code_lbl = QLabel(c.get("code", "CURS"))
            code_lbl.setStyleSheet("""
                background-color: rgba(99, 102, 241, 0.15);
                color: #a5b4fc;
                font-weight: 800;
                font-size: 11px;
                padding: 4px 10px;
                border-radius: 6px;
                border: 1px solid rgba(99, 102, 241, 0.3);
            """)
            top.addWidget(code_lbl)

            active_badge = StatusBadge("active", "Activ")
            top.addWidget(active_badge)
            top.addStretch()

            credits_lbl = QLabel(f"🎖️ {c.get('credits', 5)} ECTS")
            credits_lbl.setStyleSheet("color: #06b6d4; font-size: 12px; font-weight: 700;")
            top.addWidget(credits_lbl)
            c_layout.addLayout(top)

            # Course Title
            title_lbl = QLabel(c.get("title", ""))
            title_lbl.setStyleSheet("color: #ffffff; font-size: 16px; font-weight: 700; letter-spacing: -0.2px;")
            c_layout.addWidget(title_lbl)

            # Instructor
            instr_lbl = QLabel(f"👨‍🏫 {c.get('instructor_name', 'Instructor ArkiTech')}")
            instr_lbl.setStyleSheet("color: #94a3b8; font-size: 12px; font-weight: 500;")
            c_layout.addWidget(instr_lbl)

            if c.get("description"):
                desc_lbl = QLabel(c.get("description"))
                desc_lbl.setWordWrap(True)
                desc_lbl.setStyleSheet("color: #64748b; font-size: 12px; margin-top: 2px;")
                c_layout.addWidget(desc_lbl)

            self.courses_container.addWidget(card)

    def _render_assignments(self, assignments: list):
        while self.assignments_container.count():
            item = self.assignments_container.takeAt(0)
            if item.widget():
                item.widget().deleteLater()

        if not assignments:
            empty = EmptyState(
                icon="🎉",
                title="Toate temele sunt finalizate",
                message="Nu există teme active în așteptare."
            )
            self.assignments_container.addWidget(empty)
            return

        for a in assignments[:4]:
            item_frame = QFrame()
            item_frame.setStyleSheet("""
                QFrame {
                    background-color: #111827;
                    border: 1px solid rgba(255, 255, 255, 0.08);
                    border-radius: 10px;
                    padding: 12px 14px;
                }
                QFrame:hover {
                    border-color: rgba(245, 158, 11, 0.4);
                }
            """)
            i_layout = QVBoxLayout(item_frame)
            i_layout.setSpacing(6)

            top_row = QHBoxLayout()
            title = QLabel(a.get("title", ""))
            title.setStyleSheet("color: #f1f5f9; font-weight: 700; font-size: 13px;")
            top_row.addWidget(title)
            top_row.addStretch()

            pending_badge = StatusBadge("pending", "De predat")
            top_row.addWidget(pending_badge)
            i_layout.addLayout(top_row)

            meta_row = QHBoxLayout()
            score_lbl = QLabel(f"Punctaj maxim: {a.get('max_score', 100):.0f}p")
            score_lbl.setStyleSheet("color: #38bdf8; font-size: 11px; font-weight: 600;")
            meta_row.addWidget(score_lbl)
            meta_row.addStretch()

            due_str = a.get("due_date", "")
            if due_str:
                due_lbl = QLabel(f"Termen: {due_str[:10]}")
                due_lbl.setStyleSheet("color: #94a3b8; font-size: 11px;")
                meta_row.addWidget(due_lbl)

            i_layout.addLayout(meta_row)
            self.assignments_container.addWidget(item_frame)

    def _render_grades(self, grades: list):
        while self.grades_container.count():
            item = self.grades_container.takeAt(0)
            if item.widget():
                item.widget().deleteLater()

        if not grades:
            empty = EmptyState(
                icon="📊",
                title="Fără note recente",
                message="Notele primite vor apărea aici."
            )
            self.grades_container.addWidget(empty)
            return

        for g in grades[:4]:
            item_frame = QFrame()
            item_frame.setStyleSheet("""
                QFrame {
                    background-color: #111827;
                    border: 1px solid rgba(255, 255, 255, 0.08);
                    border-radius: 10px;
                    padding: 12px 14px;
                }
                QFrame:hover {
                    border-color: rgba(16, 185, 129, 0.4);
                }
            """)
            g_layout = QHBoxLayout(item_frame)
            g_layout.setSpacing(12)

            score = g.get("score", 0.0)
            score_badge = QLabel(f"{score:.1f}")
            score_badge.setAlignment(Qt.AlignCenter)
            score_badge.setFixedWidth(54)
            score_badge.setStyleSheet("""
                background-color: rgba(16, 185, 129, 0.15);
                color: #34d399;
                font-weight: 800;
                font-size: 15px;
                padding: 8px 6px;
                border-radius: 8px;
                border: 1px solid rgba(16, 185, 129, 0.3);
            """)
            g_layout.addWidget(score_badge)

            detail_layout = QVBoxLayout()
            detail_layout.setSpacing(3)
            fb = g.get("feedback") or "Evaluare completată cu succes"
            fb_lbl = QLabel(fb)
            fb_lbl.setStyleSheet("color: #e2e8f0; font-size: 12px; font-weight: 600;")
            detail_layout.addWidget(fb_lbl)

            date_str = g.get("graded_at", "")[:10]
            date_lbl = QLabel(f"Notat la: {date_str}")
            date_lbl.setStyleSheet("color: #64748b; font-size: 11px;")
            detail_layout.addWidget(date_lbl)

            g_layout.addLayout(detail_layout)
            self.grades_container.addWidget(item_frame)

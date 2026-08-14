from PySide6.QtWidgets import (
    QWidget, QVBoxLayout, QHBoxLayout, QLabel, QFrame, QScrollArea, QGridLayout, QTableWidget, QTableWidgetItem, QHeaderView
)
from PySide6.QtCore import Qt
from client.src.components.stat_card import StatCard
from client.src.services.api_client import api
from client.src.services.auth_service import auth


class DashboardView(QWidget):
    """Main overview dashboard with student KPIs, active courses, and upcoming assignments."""

    def __init__(self, parent=None):
        super().__init__(parent)
        self.setObjectName("DashboardView")

        # Outer Scroll Area for responsive scrolling
        outer_layout = QVBoxLayout(self)
        outer_layout.setContentsMargins(0, 0, 0, 0)

        scroll = QScrollArea()
        scroll.setWidgetResizable(True)
        scroll.setStyleSheet("QScrollArea { border: none; background-color: #0b0f19; }")

        container = QWidget()
        container.setStyleSheet("background-color: #0b0f19;")
        self.layout = QVBoxLayout(container)
        self.layout.setContentsMargins(24, 20, 24, 24)
        self.layout.setSpacing(20)

        # 1. Welcome banner
        self.welcome_banner = QFrame()
        self.welcome_banner.setStyleSheet("""
            QFrame {
                background: qlineargradient(x1:0, y1:0, x2:1, y2:0, stop:0 #1e3a8a, stop:1 #0f172a);
                border: 1px solid #1e40af;
                border-radius: 12px;
                padding: 16px 20px;
            }
        """)
        wb_layout = QVBoxLayout(self.welcome_banner)
        self.wb_title = QLabel("Bine ai revenit, Student!")
        self.wb_title.setStyleSheet("color: #ffffff; font-size: 18px; font-weight: 800;")
        self.wb_sub = QLabel("Panoul tău academic pentru semestrul curent este actualizat.")
        self.wb_sub.setStyleSheet("color: #93c5fd; font-size: 12px;")
        wb_layout.addWidget(self.wb_title)
        wb_layout.addWidget(self.wb_sub)
        self.layout.addWidget(self.welcome_banner)

        # 2. Stat KPI Cards Grid
        stats_layout = QHBoxLayout()
        stats_layout.setSpacing(16)

        self.card_courses = StatCard("Cursuri Înscrise", "0", "📚", "#3b82f6")
        self.card_credits = StatCard("Credite Totale", "0 ECTS", "🎖️", "#10b981")
        self.card_gpa = StatCard("Medie Generală", "0.0", "⭐", "#f59e0b")
        self.card_assignments = StatCard("Teme Active", "0", "📝", "#ec4899")

        stats_layout.addWidget(self.card_courses)
        stats_layout.addWidget(self.card_credits)
        stats_layout.addWidget(self.card_gpa)
        stats_layout.addWidget(self.card_assignments)

        self.layout.addLayout(stats_layout)

        # 3. Two columns: Courses Grid & Right Panel (Assignments & Grades)
        main_content = QHBoxLayout()
        main_content.setSpacing(20)

        # Left: Enrolled Courses
        left_col = QVBoxLayout()
        left_header = QLabel("Cursurile Mele Active")
        left_header.setStyleSheet("color: #f8fafc; font-size: 16px; font-weight: 700;")
        left_col.addWidget(left_header)

        self.courses_container = QVBoxLayout()
        self.courses_container.setSpacing(10)
        left_col.addLayout(self.courses_container)
        left_col.addStretch()

        main_content.addLayout(left_col, stretch=3)

        # Right: Upcoming Tasks & Recent Grades
        right_col = QVBoxLayout()
        right_col.setSpacing(16)

        # Assignments block
        assign_header = QLabel("Teme & Proiecte")
        assign_header.setStyleSheet("color: #f8fafc; font-size: 16px; font-weight: 700;")
        right_col.addWidget(assign_header)

        self.assignments_container = QVBoxLayout()
        self.assignments_container.setSpacing(8)
        right_col.addLayout(self.assignments_container)

        # Recent grades block
        grades_header = QLabel("Ultimele Note Înregistrate")
        grades_header.setStyleSheet("color: #f8fafc; font-size: 16px; font-weight: 700; margin-top: 10px;")
        right_col.addWidget(grades_header)

        self.grades_container = QVBoxLayout()
        self.grades_container.setSpacing(8)
        right_col.addLayout(self.grades_container)
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
            data = api.get(f"/students/{student_id}/dashboard")
            self._update_kpis(data)
            self._render_courses(data.get("enrolled_courses", []))
            self._render_assignments(data.get("upcoming_assignments", []))
            self._render_grades(data.get("recent_grades", []))
        except Exception as e:
            print(f"Error loading dashboard: {e}")

    def _update_kpis(self, data: dict):
        self.card_courses.set_value(str(data.get("total_enrolled_courses", 0)))
        self.card_credits.set_value(f"{data.get('total_credits', 0)} ECTS")
        self.card_gpa.set_value(f"{data.get('average_grade', 0.0):.1f} / 100")
        self.card_assignments.set_value(str(len(data.get("upcoming_assignments", []))))

    def _render_courses(self, courses: list):
        # Clear existing
        while self.courses_container.count():
            item = self.courses_container.takeAt(0)
            if item.widget():
                item.widget().deleteLater()

        if not courses:
            empty_lbl = QLabel("Nu sunteți înscris la niciun curs momentan.")
            empty_lbl.setStyleSheet("color: #64748b; padding: 20px;")
            self.courses_container.addWidget(empty_lbl)
            return

        for c in courses:
            card = QFrame()
            card.setStyleSheet("""
                QFrame {
                    background-color: #131d33;
                    border: 1px solid #1e293b;
                    border-radius: 10px;
                    padding: 14px;
                }
                QFrame:hover {
                    border-color: #3b82f6;
                }
            """)
            c_layout = QVBoxLayout(card)
            c_layout.setSpacing(6)

            top = QHBoxLayout()
            code_lbl = QLabel(c.get("code", ""))
            code_lbl.setStyleSheet("background-color: rgba(59, 130, 246, 0.15); color: #60a5fa; font-weight: 700; font-size: 11px; padding: 3px 8px; border-radius: 4px;")
            top.addWidget(code_lbl)

            credits_lbl = QLabel(f"{c.get('credits', 0)} Credite ECTS")
            credits_lbl.setStyleSheet("color: #94a3b8; font-size: 11px;")
            top.addWidget(credits_lbl)
            top.addStretch()
            c_layout.addLayout(top)

            title_lbl = QLabel(c.get("title", ""))
            title_lbl.setStyleSheet("color: #ffffff; font-size: 15px; font-weight: 700;")
            c_layout.addWidget(title_lbl)

            instr_lbl = QLabel(f"👨‍🏫 {c.get('instructor_name', 'Profesor')}")
            instr_lbl.setStyleSheet("color: #94a3b8; font-size: 12px;")
            c_layout.addWidget(instr_lbl)

            if c.get("description"):
                desc_lbl = QLabel(c.get("description"))
                desc_lbl.setWordWrap(True)
                desc_lbl.setStyleSheet("color: #64748b; font-size: 11px; margin-top: 4px;")
                c_layout.addWidget(desc_lbl)

            self.courses_container.addWidget(card)

    def _render_assignments(self, assignments: list):
        while self.assignments_container.count():
            item = self.assignments_container.takeAt(0)
            if item.widget():
                item.widget().deleteLater()

        if not assignments:
            empty_lbl = QLabel("Nicio temă activă.")
            empty_lbl.setStyleSheet("color: #64748b; font-size: 12px;")
            self.assignments_container.addWidget(empty_lbl)
            return

        for a in assignments[:4]:
            item_frame = QFrame()
            item_frame.setStyleSheet("""
                QFrame {
                    background-color: #131d33;
                    border: 1px solid #1e293b;
                    border-radius: 8px;
                    padding: 10px 12px;
                }
            """)
            i_layout = QVBoxLayout(item_frame)
            i_layout.setSpacing(4)

            title = QLabel(a.get("title", ""))
            title.setStyleSheet("color: #f8fafc; font-weight: 600; font-size: 13px;")
            i_layout.addWidget(title)

            meta = QLabel(f"Punctaj Max: {a.get('max_score', 100)}p")
            meta.setStyleSheet("color: #38bdf8; font-size: 11px;")
            i_layout.addWidget(meta)

            self.assignments_container.addWidget(item_frame)

    def _render_grades(self, grades: list):
        while self.grades_container.count():
            item = self.grades_container.takeAt(0)
            if item.widget():
                item.widget().deleteLater()

        if not grades:
            empty_lbl = QLabel("Nu există note înregistrate încă.")
            empty_lbl.setStyleSheet("color: #64748b; font-size: 12px;")
            self.grades_container.addWidget(empty_lbl)
            return

        for g in grades[:4]:
            item_frame = QFrame()
            item_frame.setStyleSheet("""
                QFrame {
                    background-color: #131d33;
                    border: 1px solid #1e293b;
                    border-radius: 8px;
                    padding: 10px 12px;
                }
            """)
            g_layout = QHBoxLayout(item_frame)
            g_layout.setSpacing(10)

            score_badge = QLabel(f"{g.get('score', 0):.1f}")
            score_badge.setStyleSheet("""
                background-color: rgba(16, 185, 129, 0.2);
                color: #34d399;
                font-weight: 800;
                font-size: 14px;
                padding: 6px 10px;
                border-radius: 6px;
            """)
            g_layout.addWidget(score_badge)

            detail_layout = QVBoxLayout()
            detail_layout.setSpacing(2)
            fb = g.get("feedback") or "Evaluare completată"
            fb_lbl = QLabel(fb)
            fb_lbl.setStyleSheet("color: #cbd5e1; font-size: 12px; font-weight: 500;")
            detail_layout.addWidget(fb_lbl)

            date_str = g.get("graded_at", "")[:10]
            date_lbl = QLabel(f"Data: {date_str}")
            date_lbl.setStyleSheet("color: #64748b; font-size: 10px;")
            detail_layout.addWidget(date_lbl)

            g_layout.addLayout(detail_layout)
            self.grades_container.addWidget(item_frame)

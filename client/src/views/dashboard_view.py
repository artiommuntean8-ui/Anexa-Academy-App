from PySide6.QtWidgets import (
    QWidget, QVBoxLayout, QHBoxLayout, QLabel, QFrame, QScrollArea, QPushButton, QProgressBar
)
from PySide6.QtCore import Qt
from PySide6.QtGui import QCursor
from client.src.components.progress_card import ProgressCard
from client.src.components.stat_card import StatCard
from client.src.components.badge import StatusBadge
from client.src.components.empty_state import EmptyState
from client.src.services.api_client import api
from client.src.services.auth_service import auth


class DashboardView(QWidget):
    """Student progress dashboard — overall percentage, metrics, and per-module progress."""

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

        # 1. Error banner
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
        self.error_msg_lbl = QLabel("Eroare de conexiune la server.")
        self.error_msg_lbl.setStyleSheet("color: #fca5a5; font-size: 12px; font-weight: 600;")
        eb_layout.addWidget(self.error_msg_lbl)
        eb_layout.addStretch()
        retry_btn = QPushButton("Reîncearcă")
        retry_btn.setCursor(QCursor(Qt.PointingHandCursor))
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
        wb_text = QVBoxLayout()
        self.wb_title = QLabel("Salut, explorator ArkiTech!")
        self.wb_title.setStyleSheet("color: #ffffff; font-size: 22px; font-weight: 800;")
        self.wb_sub = QLabel("Panoul tău academic este sincronizat în timp real.")
        self.wb_sub.setStyleSheet("color: #a5b4fc; font-size: 13px; font-weight: 500;")
        wb_text.addWidget(self.wb_title)
        wb_text.addWidget(self.wb_sub)
        wb_layout.addLayout(wb_text)
        wb_layout.addStretch()
        hero = QLabel("🎓")
        hero.setStyleSheet("font-size: 40px;")
        wb_layout.addWidget(hero)
        self.layout.addWidget(self.welcome_banner)

        # 3. KPI Stat Cards Row
        stats_layout = QHBoxLayout()
        stats_layout.setSpacing(16)
        self.card_courses = StatCard("Cursuri Active", "0", "📚", "#6366f1", "rgba(99, 102, 241, 0.12)", "Semestrul curent")
        self.card_assignments = StatCard("Teme Finalizate", "0", "📝", "#10b981", "rgba(16, 185, 129, 0.12)", "Lecții notate")
        self.card_gpa = StatCard("Medie Generală", "0.0", "⭐", "#06b6d4", "rgba(6, 182, 212, 0.12)", "Punctaj academic")

        stats_layout.addWidget(self.card_courses)
        stats_layout.addWidget(self.card_assignments)
        stats_layout.addWidget(self.card_gpa)
        self.layout.addLayout(stats_layout)

        # 4. Academic Progress Card
        self.progress_card = ProgressCard()
        self.layout.addWidget(self.progress_card)

        # 5. Modules List Header & Container
        modules_header = QLabel("Modulele și Cursurile Tale")
        modules_header.setStyleSheet("color: #ffffff; font-size: 18px; font-weight: 800; letter-spacing: -0.2px;")
        self.layout.addWidget(modules_header)

        self.modules_container = QVBoxLayout()
        self.modules_container.setSpacing(12)
        self.layout.addLayout(self.modules_container)
        self.layout.addStretch()

        scroll.setWidget(container)
        outer_layout.addWidget(scroll)

    def refresh_data(self):
        user = auth.current_user
        if not user:
            return

        student_id = user.get("id")
        self.wb_title.setText(f"Salut, {user.get('full_name', 'Student')}! 🎉")
        self.wb_sub.setText(f"Departament: {user.get('department', 'Software Engineering')} • Semestrul {user.get('semester', 1)}")

        try:
            self.error_banner.hide()
            dash = api.get(f"/students/{student_id}/dashboard")
            enrolled = dash.get("enrolled_courses", [])
            avg_grade = dash.get("average_grade", 0.0)
            total_credits = dash.get("total_credits", 0)

            # Update KPI Cards
            self.card_courses.set_value(str(len(enrolled)))
            self.card_gpa.set_value(f"{avg_grade:.1f}" if avg_grade > 0 else "-")

            # Try to get progress metrics
            try:
                prog = api.get("/students/me/progress")
                completed = prog.get("completed_lessons", 0)
                total = prog.get("total_lessons", max(1, len(enrolled) * 4))
                pct = prog.get("overall_progress_percent", 0)
                modules_data = prog.get("modules", [])
            except Exception:
                completed = len(dash.get("recent_grades", []))
                total = max(1, len(enrolled) * 4)
                pct = int((completed / total) * 100) if total else 0
                modules_data = []

            self.card_assignments.set_value(str(completed))
            self.progress_card.set_progress(current_credits=total_credits, total_target_credits=30, gpa=avg_grade)

            self._render_modules(modules_data if modules_data else enrolled)

        except Exception as e:
            self.error_msg_lbl.setText(f"Eroare: {str(e)}")
            self.error_banner.show()

    def _render_modules(self, modules: list):
        while self.modules_container.count():
            item = self.modules_container.takeAt(0)
            if item.widget():
                item.widget().deleteLater()

        if not modules:
            self.modules_container.addWidget(EmptyState(
                icon="📚",
                title="Niciun modul încă",
                message="Accesează catalogul de cursuri pentru a te înscrie la materii.",
            ))
            return

        for module in modules:
            card = QFrame()
            card.setStyleSheet("""
                QFrame {
                    background-color: #111827;
                    border: 1px solid rgba(255, 255, 255, 0.08);
                    border-radius: 14px;
                    padding: 16px 18px;
                }
                QFrame:hover {
                    border-color: rgba(99, 102, 241, 0.4);
                    background-color: #131c2e;
                }
            """)
            c_layout = QVBoxLayout(card)
            c_layout.setSpacing(10)

            top = QHBoxLayout()
            code_str = module.get("module_code") or module.get("code", "CURS")
            code = QLabel(code_str)
            code.setStyleSheet("""
                background-color: rgba(99, 102, 241, 0.15);
                color: #a5b4fc;
                font-weight: 800;
                font-size: 11px;
                padding: 4px 10px;
                border-radius: 6px;
                border: 1px solid rgba(99, 102, 241, 0.3);
            """)
            top.addWidget(code)

            title_str = module.get("module_title") or module.get("title", "")
            title = QLabel(title_str)
            title.setStyleSheet("color: #ffffff; font-size: 15px; font-weight: 700;")
            top.addWidget(title)
            top.addStretch()

            pct = int(round(module.get("progress_percent", 50)))
            pct_lbl = QLabel(f"{pct}%")
            pct_lbl.setStyleSheet("color: #34d399; font-size: 16px; font-weight: 800;")
            top.addWidget(pct_lbl)
            c_layout.addLayout(top)

            bar = QProgressBar()
            bar.setRange(0, 100)
            bar.setValue(pct)
            bar.setFixedHeight(8)
            bar.setTextVisible(False)
            bar.setStyleSheet("""
                QProgressBar { background-color: #1f293d; border-radius: 4px; }
                QProgressBar::chunk {
                    background: qlineargradient(x1:0, y1:0, x2:1, y2:0, stop:0 #4f46e5, stop:1 #06b6d4);
                    border-radius: 4px;
                }
            """)
            c_layout.addWidget(bar)

            desc = module.get("description", "")
            if desc:
                info = QLabel(desc)
                info.setStyleSheet("color: #94a3b8; font-size: 12px;")
                c_layout.addWidget(info)

            self.modules_container.addWidget(card)

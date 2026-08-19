from PySide6.QtWidgets import (
    QWidget, QVBoxLayout, QHBoxLayout, QLabel, QFrame, QScrollArea, QPushButton, QProgressBar
)
from PySide6.QtCore import Qt
from PySide6.QtGui import QCursor
from client.src.components.progress_card import ProgressCard
from client.src.components.empty_state import EmptyState
from client.src.services.api_client import api
from client.src.services.auth_service import auth


class DashboardView(QWidget):
    """Student progress dashboard — overall percentage and per-module progress."""

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
        self.error_msg_lbl = QLabel("Eroare de conexiune.")
        self.error_msg_lbl.setStyleSheet("color: #fca5a5; font-size: 12px; font-weight: 600;")
        eb_layout.addWidget(self.error_msg_lbl)
        eb_layout.addStretch()
        retry_btn = QPushButton("Reîncearcă")
        retry_btn.setCursor(QCursor(Qt.PointingHandCursor))
        retry_btn.clicked.connect(self.refresh_data)
        eb_layout.addWidget(retry_btn)
        self.error_banner.hide()
        self.layout.addWidget(self.error_banner)

        self.welcome_banner = QFrame()
        self.welcome_banner.setStyleSheet("""
            QFrame {
                background: qlineargradient(x1:0, y1:0, x2:1, y2:0, stop:0 #064e3b, stop:0.5 #0e7490, stop:1 #1e1b4b);
                border: 1px solid rgba(16, 185, 129, 0.3);
                border-radius: 16px;
                padding: 20px 24px;
            }
        """)
        wb_layout = QHBoxLayout(self.welcome_banner)
        wb_text = QVBoxLayout()
        self.wb_title = QLabel("Salut, explorator Python!")
        self.wb_title.setStyleSheet("color: #ffffff; font-size: 22px; font-weight: 800;")
        self.wb_sub = QLabel("Urmărește progresul tău lecție cu lecție.")
        self.wb_sub.setStyleSheet("color: #a7f3d0; font-size: 14px; font-weight: 500;")
        wb_text.addWidget(self.wb_title)
        wb_text.addWidget(self.wb_sub)
        wb_layout.addLayout(wb_text)
        wb_layout.addStretch()
        hero = QLabel("🐍")
        hero.setStyleSheet("font-size: 42px;")
        wb_layout.addWidget(hero)
        self.layout.addWidget(self.welcome_banner)

        self.progress_card = ProgressCard()
        self.layout.addWidget(self.progress_card)

        modules_header = QLabel("Modulele tale Python")
        modules_header.setStyleSheet("color: #ffffff; font-size: 17px; font-weight: 800;")
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

        self.wb_title.setText(f"Salut, {user.get('full_name', 'explorator')}! 🎉")
        self.wb_sub.setText(f"Grupă: {user.get('department', 'Python Kids')}")

        try:
            self.error_banner.hide()
            data = api.get("/students/me/progress")
            self.progress_card.set_progress(
                completed=data.get("completed_lessons", 0),
                total=data.get("total_lessons", 0),
                percent=data.get("overall_progress_percent", 0),
            )
            self._render_modules(data.get("modules", []))
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
                message="Profesoara va adăuga modulele Python curând.",
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
            """)
            c_layout = QVBoxLayout(card)
            c_layout.setSpacing(10)

            top = QHBoxLayout()
            code = QLabel(module.get("module_code", ""))
            code.setStyleSheet("""
                background-color: rgba(16, 185, 129, 0.15);
                color: #6ee7b7;
                font-weight: 800;
                font-size: 11px;
                padding: 4px 10px;
                border-radius: 6px;
            """)
            top.addWidget(code)

            title = QLabel(module.get("module_title", ""))
            title.setStyleSheet("color: #ffffff; font-size: 15px; font-weight: 700;")
            top.addWidget(title)
            top.addStretch()

            pct = int(round(module.get("progress_percent", 0)))
            pct_lbl = QLabel(f"{pct}%")
            pct_lbl.setStyleSheet("color: #34d399; font-size: 18px; font-weight: 900;")
            top.addWidget(pct_lbl)
            c_layout.addLayout(top)

            bar = QProgressBar()
            bar.setRange(0, 100)
            bar.setValue(pct)
            bar.setFixedHeight(10)
            bar.setTextVisible(False)
            bar.setStyleSheet("""
                QProgressBar { background-color: #1f293d; border-radius: 5px; }
                QProgressBar::chunk {
                    background: qlineargradient(x1:0, y1:0, x2:1, y2:0, stop:0 #10b981, stop:1 #06b6d4);
                    border-radius: 5px;
                }
            """)
            c_layout.addWidget(bar)

            info = QLabel(
                f"Lecții: {module.get('completed_lessons', 0)} / {module.get('total_lessons', 0)} completate"
            )
            info.setStyleSheet("color: #94a3b8; font-size: 12px;")
            c_layout.addWidget(info)

            self.modules_container.addWidget(card)

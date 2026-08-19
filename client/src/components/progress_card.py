from PySide6.QtWidgets import QFrame, QVBoxLayout, QHBoxLayout, QLabel, QProgressBar
from PySide6.QtCore import Qt


class ProgressCard(QFrame):
    """Kid-friendly progress card with large percentage display."""

    def __init__(self, parent=None):
        super().__init__(parent)
        self.setObjectName("ProgressCard")
        self.setStyleSheet("""
            QFrame#ProgressCard {
                background-color: #111827;
                border: 1px solid rgba(255, 255, 255, 0.08);
                border-radius: 16px;
                padding: 20px 24px;
            }
        """)

        layout = QVBoxLayout(self)
        layout.setContentsMargins(20, 18, 20, 18)
        layout.setSpacing(14)

        top_layout = QHBoxLayout()
        title_lbl = QLabel("🐍 Progresul tău la Python")
        title_lbl.setStyleSheet("color: #f1f5f9; font-size: 18px; font-weight: 800;")
        top_layout.addWidget(title_lbl)
        top_layout.addStretch()

        self.percentage_badge = QLabel("0%")
        self.percentage_badge.setStyleSheet("""
            background-color: rgba(16, 185, 129, 0.15);
            color: #34d399;
            font-weight: 900;
            font-size: 28px;
            padding: 8px 18px;
            border-radius: 12px;
            border: 2px solid rgba(16, 185, 129, 0.35);
        """)
        top_layout.addWidget(self.percentage_badge)
        layout.addLayout(top_layout)

        self.progress_bar = QProgressBar()
        self.progress_bar.setRange(0, 100)
        self.progress_bar.setValue(0)
        self.progress_bar.setFixedHeight(18)
        self.progress_bar.setTextVisible(False)
        self.progress_bar.setStyleSheet("""
            QProgressBar {
                background-color: #1f293d;
                border-radius: 9px;
            }
            QProgressBar::chunk {
                background: qlineargradient(x1:0, y1:0, x2:1, y2:0, stop:0 #10b981, stop:0.5 #06b6d4, stop:1 #6366f1);
                border-radius: 9px;
            }
        """)
        layout.addWidget(self.progress_bar)

        bottom_layout = QHBoxLayout()
        self.lessons_info = QLabel("Lecții completate: 0 / 0")
        self.lessons_info.setStyleSheet("color: #94a3b8; font-size: 14px; font-weight: 600;")
        bottom_layout.addWidget(self.lessons_info)
        bottom_layout.addStretch()

        self.status_info = QLabel("Continuă! Ești pe drumul cel bun 🚀")
        self.status_info.setStyleSheet("color: #34d399; font-size: 13px; font-weight: 700;")
        bottom_layout.addWidget(self.status_info)
        layout.addLayout(bottom_layout)

    def set_progress(self, completed: int, total: int, percent: float):
        pct = int(round(percent))
        self.progress_bar.setValue(pct)
        self.percentage_badge.setText(f"{pct}%")
        self.lessons_info.setText(f"Lecții completate: {completed} / {total}")

        if pct >= 80:
            self.status_info.setText("Super! Ești aproape de final! 🏆")
            self.status_info.setStyleSheet("color: #34d399; font-size: 13px; font-weight: 700;")
        elif pct >= 40:
            self.status_info.setText("Foarte bine! Continuă așa! 🚀")
            self.status_info.setStyleSheet("color: #38bdf8; font-size: 13px; font-weight: 700;")
        elif pct > 0:
            self.status_info.setText("Ai început! Fiecare lecție contează 💪")
            self.status_info.setStyleSheet("color: #fbbf24; font-size: 13px; font-weight: 700;")
        else:
            self.status_info.setText("Hai să începem aventura Python! 🐍")
            self.status_info.setStyleSheet("color: #94a3b8; font-size: 13px; font-weight: 700;")

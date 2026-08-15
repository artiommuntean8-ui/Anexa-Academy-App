from PySide6.QtWidgets import QFrame, QVBoxLayout, QHBoxLayout, QLabel, QProgressBar
from PySide6.QtCore import Qt


class ProgressCard(QFrame):
    """Academic Progress Card with modern gradient Progress Bar and semester KPIs."""

    def __init__(self, parent=None):
        super().__init__(parent)
        self.setObjectName("ProgressCard")
        self.setStyleSheet("""
            QFrame#ProgressCard {
                background-color: #111827;
                border: 1px solid rgba(255, 255, 255, 0.08);
                border-radius: 14px;
                padding: 16px 20px;
            }
            QFrame#ProgressCard:hover {
                border-color: rgba(99, 102, 241, 0.4);
            }
        """)

        layout = QVBoxLayout(self)
        layout.setContentsMargins(18, 16, 18, 16)
        layout.setSpacing(12)

        # Header Row
        top_layout = QHBoxLayout()
        top_layout.setContentsMargins(0, 0, 0, 0)

        title_lbl = QLabel("Progres Academic Semestrial")
        title_lbl.setStyleSheet("color: #f1f5f9; font-size: 14px; font-weight: 700;")
        top_layout.addWidget(title_lbl)
        top_layout.addStretch()

        self.percentage_badge = QLabel("0%")
        self.percentage_badge.setStyleSheet("""
            background-color: rgba(99, 102, 241, 0.15);
            color: #818cf8;
            font-weight: 800;
            font-size: 12px;
            padding: 3px 10px;
            border-radius: 6px;
            border: 1px solid rgba(99, 102, 241, 0.3);
        """)
        top_layout.addWidget(self.percentage_badge)
        layout.addLayout(top_layout)

        # Progress Bar
        self.progress_bar = QProgressBar()
        self.progress_bar.setRange(0, 100)
        self.progress_bar.setValue(0)
        self.progress_bar.setFixedHeight(8)
        self.progress_bar.setTextVisible(False)
        self.progress_bar.setStyleSheet("""
            QProgressBar {
                background-color: #1f293d;
                border-radius: 4px;
            }
            QProgressBar::chunk {
                background: qlineargradient(x1:0, y1:0, x2:1, y2:0, stop:0 #4f46e5, stop:1 #06b6d4);
                border-radius: 4px;
            }
        """)
        layout.addWidget(self.progress_bar)

        # Bottom metrics
        bottom_layout = QHBoxLayout()
        bottom_layout.setContentsMargins(0, 0, 0, 0)

        self.credits_info = QLabel("Credite acumulate: 0 / 30 ECTS")
        self.credits_info.setStyleSheet("color: #94a3b8; font-size: 12px; font-weight: 500;")
        bottom_layout.addWidget(self.credits_info)
        bottom_layout.addStretch()

        self.status_info = QLabel("Stare: În grafic normal")
        self.status_info.setStyleSheet("color: #34d399; font-size: 12px; font-weight: 600;")
        bottom_layout.addWidget(self.status_info)

        layout.addLayout(bottom_layout)

    def set_progress(self, current_credits: int, total_target_credits: int = 30, gpa: float = 0.0):
        percent = min(100, int((current_credits / max(1, total_target_credits)) * 100))
        self.progress_bar.setValue(percent)
        self.percentage_badge.setText(f"{percent}%")
        self.credits_info.setText(f"Credite acumulate: {current_credits} / {total_target_credits} ECTS")

        if gpa >= 90:
            self.status_info.setText("Stare: Performanță Excelentă ⭐")
            self.status_info.setStyleSheet("color: #34d399; font-size: 12px; font-weight: 600;")
        elif gpa >= 70:
            self.status_info.setText("Stare: În Grafic Bun ✓")
            self.status_info.setStyleSheet("color: #38bdf8; font-size: 12px; font-weight: 600;")
        else:
            self.status_info.setText("Stare: Atenție Necesară ⚠️")
            self.status_info.setStyleSheet("color: #fbbf24; font-size: 12px; font-weight: 600;")

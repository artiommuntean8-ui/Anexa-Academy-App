from PySide6.QtWidgets import QWidget, QVBoxLayout, QHBoxLayout, QLabel, QProgressBar, QFrame
from PySide6.QtCore import Qt


class XPBar(QFrame):
    """Visual XP and Level Rank progress component."""

    def __init__(self, parent=None):
        super().__init__(parent)
        self.setObjectName("XPBar")
        self.setStyleSheet("""
            QFrame#XPBar {
                background: qlineargradient(x1:0, y1:0, x2:1, y2:0, stop:0 #1e1b4b, stop:0.5 #312e81, stop:1 #111827);
                border: 1px solid rgba(99, 102, 241, 0.35);
                border-radius: 14px;
                padding: 14px 18px;
            }
        """)

        layout = QVBoxLayout(self)
        layout.setContentsMargins(0, 0, 0, 0)
        layout.setSpacing(8)

        # Top row: Rank Title + Level Badge + XP stats
        top_row = QHBoxLayout()
        top_row.setSpacing(10)

        self.rank_icon = QLabel("⚡")
        self.rank_icon.setStyleSheet("font-size: 20px;")
        top_row.addWidget(self.rank_icon)

        self.rank_lbl = QLabel("Începător Python")
        self.rank_lbl.setStyleSheet("color: #ffffff; font-size: 14px; font-weight: 800; letter-spacing: -0.2px;")
        top_row.addWidget(self.rank_lbl)

        self.level_badge = QLabel("NIVEL 1")
        self.level_badge.setStyleSheet("""
            background-color: #4f46e5;
            color: #ffffff;
            font-size: 10px;
            font-weight: 800;
            padding: 3px 8px;
            border-radius: 6px;
            letter-spacing: 0.5px;
        """)
        top_row.addWidget(self.level_badge)

        top_row.addStretch()

        self.xp_fraction_lbl = QLabel("0 / 200 XP")
        self.xp_fraction_lbl.setStyleSheet("color: #a5b4fc; font-size: 12px; font-weight: 700;")
        top_row.addWidget(self.xp_fraction_lbl)

        layout.addLayout(top_row)

        # Progress bar
        self.bar = QProgressBar()
        self.bar.setRange(0, 100)
        self.bar.setValue(0)
        self.bar.setFixedHeight(8)
        self.bar.setTextVisible(False)
        self.bar.setStyleSheet("""
            QProgressBar {
                background-color: rgba(15, 23, 42, 0.6);
                border-radius: 4px;
                border: none;
            }
            QProgressBar::chunk {
                background: qlineargradient(x1:0, y1:0, x2:1, y2:0, stop:0 #6366f1, stop:0.7 #06b6d4, stop:1 #10b981);
                border-radius: 4px;
            }
        """)
        layout.addWidget(self.bar)

    def set_stats(self, level: int, title: str, xp_in_level: int, next_level_xp: int = 200, total_xp: int = 0):
        self.level_badge.setText(f"NIVEL {level}")
        self.rank_lbl.setText(title)
        self.xp_fraction_lbl.setText(f"{total_xp} XP ({xp_in_level}/{next_level_xp} XP)")
        pct = min(100, int((xp_in_level / next_level_xp) * 100)) if next_level_xp > 0 else 0
        self.bar.setValue(pct)

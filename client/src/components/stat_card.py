from PySide6.QtWidgets import QFrame, QVBoxLayout, QHBoxLayout, QLabel
from PySide6.QtCore import Qt


class StatCard(QFrame):
    """Modern Obsidian Glass KPI metric card with tinted glowing icon box."""

    def __init__(self, title: str, value: str, icon: str, accent_color: str = "#6366f1", bg_tint: str = "rgba(99, 102, 241, 0.12)", subtitle: str = "", parent=None):
        super().__init__(parent)
        self.setObjectName("StatCard")

        self.setStyleSheet(f"""
            QFrame#StatCard {{
                background-color: #0e1424;
                border: 1px solid rgba(255, 255, 255, 0.07);
                border-radius: 16px;
                padding: 16px 18px;
            }}
            QFrame#StatCard:hover {{
                background-color: #12192e;
                border: 1px solid rgba(255, 255, 255, 0.14);
            }}
        """)

        layout = QVBoxLayout(self)
        layout.setContentsMargins(0, 0, 0, 0)
        layout.setSpacing(10)

        # Top row: Title + Glowing Icon Box
        top_row = QHBoxLayout()
        top_row.setSpacing(10)

        title_lbl = QLabel(title.upper())
        title_lbl.setStyleSheet("color: #64748b; font-size: 11px; font-weight: 800; letter-spacing: 0.8px;")
        top_row.addWidget(title_lbl)
        top_row.addStretch()

        # Icon box
        icon_box = QFrame()
        icon_box.setFixedSize(36, 36)
        icon_box.setStyleSheet(f"""
            QFrame {{
                background-color: {bg_tint};
                border: 1px solid {accent_color}40;
                border-radius: 10px;
            }}
        """)
        ib_layout = QVBoxLayout(icon_box)
        ib_layout.setContentsMargins(0, 0, 0, 0)
        ib_layout.setAlignment(Qt.AlignCenter)

        icon_lbl = QLabel(icon)
        icon_lbl.setAlignment(Qt.AlignCenter)
        icon_lbl.setStyleSheet(f"font-size: 17px; color: {accent_color};")
        ib_layout.addWidget(icon_lbl)
        top_row.addWidget(icon_box)

        layout.addLayout(top_row)

        # Value Row
        self.val_lbl = QLabel(value)
        self.val_lbl.setStyleSheet("color: #ffffff; font-size: 24px; font-weight: 900; letter-spacing: -0.5px;")
        layout.addWidget(self.val_lbl)

        # Subtitle Context Row
        if subtitle:
            sub_row = QHBoxLayout()
            sub_row.setSpacing(6)
            self.sub_lbl = QLabel(subtitle)
            self.sub_lbl.setStyleSheet("color: #94a3b8; font-size: 11px; font-weight: 500;")
            sub_row.addWidget(self.sub_lbl)
            sub_row.addStretch()
            layout.addLayout(sub_row)

    def set_value(self, value: str):
        self.val_lbl.setText(value)

    def set_subtitle(self, subtitle: str):
        if hasattr(self, 'sub_lbl'):
            self.sub_lbl.setText(subtitle)

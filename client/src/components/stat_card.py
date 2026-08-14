from PySide6.QtWidgets import QFrame, QVBoxLayout, QLabel, QHBoxLayout
from PySide6.QtCore import Qt


class StatCard(QFrame):
    """Modern KPI metric card component."""

    def __init__(self, title: str, value: str, icon_str: str = "📈", accent_color: str = "#3b82f6", parent=None):
        super().__init__(parent)
        self.setObjectName("StatCard")
        self.setProperty("class", "Card")
        self.setStyleSheet(f"""
            QFrame#StatCard {{
                background-color: #131d33;
                border: 1px solid #1e293b;
                border-radius: 12px;
                padding: 16px;
            }}
            QFrame#StatCard:hover {{
                border: 1px solid {accent_color};
            }}
        """)

        layout = QVBoxLayout(self)
        layout.setContentsMargins(18, 16, 18, 16)
        layout.setSpacing(8)

        # Top row: icon + title
        top_layout = QHBoxLayout()
        top_layout.setContentsMargins(0, 0, 0, 0)

        icon_label = QLabel(icon_str)
        icon_label.setStyleSheet("font-size: 20px;")
        top_layout.addWidget(icon_label)

        title_label = QLabel(title)
        title_label.setStyleSheet("color: #94a3b8; font-size: 12px; font-weight: 600; text-transform: uppercase; letter-spacing: 0.5px;")
        top_layout.addWidget(title_label)
        top_layout.addStretch()

        layout.addLayout(top_layout)

        # Value label
        self.val_label = QLabel(value)
        self.val_label.setStyleSheet(f"font-size: 28px; font-weight: 800; color: #ffffff;")
        layout.addWidget(self.val_label)

    def set_value(self, new_value: str) -> None:
        self.val_label.setText(new_value)

from PySide6.QtWidgets import QFrame, QVBoxLayout, QLabel, QHBoxLayout
from PySide6.QtCore import Qt


class StatCard(QFrame):
    """Modern SaaS Metric KPI Card with icon container, dynamic values, and context chips."""

    def __init__(
        self,
        title: str,
        value: str,
        icon_str: str = "📊",
        accent_color: str = "#6366f1",
        accent_bg: str = "rgba(99, 102, 241, 0.12)",
        context_text: str = "",
        parent=None
    ):
        super().__init__(parent)
        self.setObjectName("StatCard")
        self.setProperty("class", "Card")
        self.accent_color = accent_color

        self.setStyleSheet(f"""
            QFrame#StatCard {{
                background-color: #111827;
                border: 1px solid rgba(255, 255, 255, 0.08);
                border-radius: 14px;
            }}
            QFrame#StatCard:hover {{
                border: 1px solid {accent_color};
                background-color: #131c2e;
            }}
        """)

        layout = QVBoxLayout(self)
        layout.setContentsMargins(18, 16, 18, 16)
        layout.setSpacing(12)

        # Top row: Title + Icon badge container
        top_layout = QHBoxLayout()
        top_layout.setContentsMargins(0, 0, 0, 0)

        title_layout = QVBoxLayout()
        title_layout.setSpacing(2)

        title_label = QLabel(title)
        title_label.setStyleSheet("color: #94a3b8; font-size: 11px; font-weight: 700; text-transform: uppercase; letter-spacing: 0.6px;")
        title_layout.addWidget(title_label)

        self.val_label = QLabel(value)
        self.val_label.setStyleSheet("font-size: 26px; font-weight: 800; color: #ffffff; letter-spacing: -0.5px;")
        title_layout.addWidget(self.val_label)

        top_layout.addLayout(title_layout)
        top_layout.addStretch()

        # Icon box
        icon_box = QFrame()
        icon_box.setFixedSize(44, 44)
        icon_box.setStyleSheet(f"""
            QFrame {{
                background-color: {accent_bg};
                border: 1px solid {accent_color}33;
                border-radius: 10px;
            }}
        """)
        ib_layout = QVBoxLayout(icon_box)
        ib_layout.setContentsMargins(0, 0, 0, 0)
        ib_layout.setAlignment(Qt.AlignCenter)
        
        icon_label = QLabel(icon_str)
        icon_label.setAlignment(Qt.AlignCenter)
        icon_label.setStyleSheet("font-size: 20px;")
        ib_layout.addWidget(icon_label)
        top_layout.addWidget(icon_box)

        layout.addLayout(top_layout)

        # Bottom context / subtitle if provided
        if context_text:
            self.ctx_label = QLabel(context_text)
            self.ctx_label.setStyleSheet("color: #64748b; font-size: 11px; font-weight: 500;")
            layout.addWidget(self.ctx_label)
        else:
            self.ctx_label = None

    def set_value(self, new_value: str) -> None:
        self.val_label.setText(new_value)

    def set_context(self, new_context: str) -> None:
        if self.ctx_label:
            self.ctx_label.setText(new_context)

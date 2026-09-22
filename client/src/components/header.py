from PySide6.QtWidgets import QWidget, QHBoxLayout, QVBoxLayout, QLabel, QPushButton, QFrame
from PySide6.QtCore import Qt, Signal, QSizePolicy
from PySide6.QtGui import QCursor, QFont
import logging
from client.src.styles.theme import COLORS

logger = logging.getLogger("client.header")


class Header(QWidget):
    """Modern top navigation bar component for page titles, server status badge, and actions."""

    refresh_requested = Signal()

    def __init__(self, parent=None):
        super().__init__(parent)
        self.setObjectName("Header")
        self.setSizePolicy(QSizePolicy.Expanding, QSizePolicy.Fixed)
        self.setMinimumHeight(70)
        self.setStyleSheet(f"""
            QWidget#Header {{
                background-color: {COLORS['bg_window_secondary']};
                border-bottom: 1px solid {COLORS['border']};
            }}
        """)

        layout = QHBoxLayout(self)
        layout.setContentsMargins(28, 16, 28, 16)
        layout.setSpacing(20)

        # Title & Subtitle with breadcrumb
        text_layout = QVBoxLayout()
        text_layout.setSpacing(4)
        text_layout.setContentsMargins(0, 0, 0, 0)

        self.breadcrumb_label = QLabel("ARKITECH PORTAL  /  PANOU PRINCIPAL")
        self.breadcrumb_label.setStyleSheet(f"color: {COLORS['accent']}; font-size: 11px; font-weight: 700; letter-spacing: 1px; background: transparent;")
        text_layout.addWidget(self.breadcrumb_label)

        self.title_label = QLabel("Tablou de bord")
        self.title_label.setObjectName("HeaderTitle")
        self.title_label.setStyleSheet(f"color: {COLORS['text_primary']}; font-size: 20px; font-weight: 800; letter-spacing: -0.5px; background: transparent;")
        text_layout.addWidget(self.title_label)

        self.subtitle_label = QLabel("Sinteza academică și performanța semestrială curentă")
        self.subtitle_label.setObjectName("HeaderSubtitle")
        self.subtitle_label.setStyleSheet(f"color: {COLORS['text_muted']}; font-size: 13px; font-weight: 500; background: transparent;")
        text_layout.addWidget(self.subtitle_label)

        layout.addLayout(text_layout)
        layout.addStretch()

        # Server status badge
        status_frame = QFrame()
        status_frame.setStyleSheet(f"""
            QFrame {{
                background-color: {COLORS['success_bg']};
                border: 1px solid {COLORS['success']};
                border-radius: 8px;
                padding: 8px 16px;
            }}
        """)
        status_layout = QHBoxLayout(status_frame)
        status_layout.setContentsMargins(0, 0, 0, 0)
        status_layout.setSpacing(8)

        dot = QLabel("●")
        dot.setStyleSheet(f"color: {COLORS['success']}; font-size: 12px; background: transparent;")
        status_layout.addWidget(dot)

        status_text = QLabel("API Conectat")
        status_text.setStyleSheet(f"color: {COLORS['success']}; font-size: 12px; font-weight: 700; background: transparent;")
        status_layout.addWidget(status_text)
        layout.addWidget(status_frame)

        # Refresh button
        self.refresh_btn = QPushButton("🔄 Sincronizează")
        self.refresh_btn.setCursor(QCursor(Qt.PointingHandCursor))
        self.refresh_btn.setSizePolicy(QSizePolicy.Fixed, QSizePolicy.Fixed)
        self.refresh_btn.setMinimumWidth(140)
        self.refresh_btn.setStyleSheet(f"""
            QPushButton {{
                background-color: {COLORS['bg_card']};
                color: {COLORS['text_secondary']};
                border: 1px solid {COLORS['border']};
                border-radius: 8px;
                padding: 10px 16px;
                font-size: 13px;
                font-weight: 600;
            }}
            QPushButton:hover {{
                background-color: {COLORS['bg_card_hover']};
                color: {COLORS['text_primary']};
                border-color: {COLORS['accent']};
            }}
            QPushButton:pressed {{
                background-color: {COLORS['accent']};
                color: {COLORS['text_primary']};
            }}
        """)
        self.refresh_btn.clicked.connect(self.refresh_requested.emit)
        layout.addWidget(self.refresh_btn)

    def set_title(self, title: str, subtitle: str = "", breadcrumb: str = ""):
        try:
            self.title_label.setText(title)
            if subtitle:
                self.subtitle_label.setText(subtitle)
            if breadcrumb:
                self.breadcrumb_label.setText(f"ARKITECH PORTAL  /  {breadcrumb.upper()}")
            else:
                self.breadcrumb_label.setText(f"ARKITECH PORTAL  /  {title.upper()}")
        except Exception as e:
            logger.error(f"Error setting header title: {e}")

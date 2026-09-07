from PySide6.QtWidgets import QWidget, QHBoxLayout, QVBoxLayout, QLabel, QPushButton, QFrame
from PySide6.QtCore import Qt, Signal
from PySide6.QtGui import QCursor


class Header(QWidget):
    """Modern top navigation bar component for page titles, server status badge, and actions."""

    refresh_requested = Signal()

    def __init__(self, parent=None):
        super().__init__(parent)
        self.setObjectName("Header")
        self.setStyleSheet("""
            QWidget#Header {
                background-color: #080b11;
                border-bottom: 1px solid rgba(255, 255, 255, 0.06);
            }
        """)

        layout = QHBoxLayout(self)
        layout.setContentsMargins(28, 16, 28, 16)
        layout.setSpacing(16)

        # Title & Subtitle with breadcrumb
        text_layout = QVBoxLayout()
        text_layout.setSpacing(3)

        self.breadcrumb_label = QLabel("ARKITECH PORTAL  /  PANOU PRINCIPAL")
        self.breadcrumb_label.setStyleSheet("color: #818cf8; font-size: 10px; font-weight: 800; letter-spacing: 0.8px;")
        text_layout.addWidget(self.breadcrumb_label)

        self.title_label = QLabel("Tablou de bord")
        self.title_label.setObjectName("HeaderTitle")
        self.title_label.setStyleSheet("color: #ffffff; font-size: 22px; font-weight: 900; letter-spacing: -0.4px;")
        text_layout.addWidget(self.title_label)

        self.subtitle_label = QLabel("Sinteza academică și performanța semestrială curentă")
        self.subtitle_label.setObjectName("HeaderSubtitle")
        self.subtitle_label.setStyleSheet("color: #64748b; font-size: 12px; font-weight: 500;")
        text_layout.addWidget(self.subtitle_label)

        layout.addLayout(text_layout)
        layout.addStretch()

        # Server status badge
        status_frame = QFrame()
        status_frame.setStyleSheet("""
            QFrame {
                background-color: rgba(16, 185, 129, 0.08);
                border: 1px solid rgba(16, 185, 129, 0.25);
                border-radius: 8px;
                padding: 6px 12px;
            }
        """)
        status_layout = QHBoxLayout(status_frame)
        status_layout.setContentsMargins(4, 2, 4, 2)
        status_layout.setSpacing(8)

        dot = QLabel("●")
        dot.setStyleSheet("color: #10b981; font-size: 10px;")
        status_layout.addWidget(dot)

        status_text = QLabel("API Conectat")
        status_text.setStyleSheet("color: #34d399; font-size: 11px; font-weight: 800;")
        status_layout.addWidget(status_text)
        layout.addWidget(status_frame)

        # Refresh button
        self.refresh_btn = QPushButton("🔄  Sincronizează")
        self.refresh_btn.setCursor(QCursor(Qt.PointingHandCursor))
        self.refresh_btn.setStyleSheet("""
            QPushButton {
                background-color: #111728;
                color: #e2e8f0;
                border: 1px solid rgba(255, 255, 255, 0.08);
                border-radius: 8px;
                padding: 8px 14px;
                font-size: 12px;
                font-weight: 700;
            }
            QPushButton:hover {
                background-color: #1b243d;
                color: #ffffff;
                border-color: rgba(255, 255, 255, 0.2);
            }
        """)
        self.refresh_btn.clicked.connect(self.refresh_requested.emit)
        layout.addWidget(self.refresh_btn)

    def set_title(self, title: str, subtitle: str = "", breadcrumb: str = ""):
        self.title_label.setText(title)
        if subtitle:
            self.subtitle_label.setText(subtitle)
        if breadcrumb:
            self.breadcrumb_label.setText(f"ARKITECH PORTAL  /  {breadcrumb.upper()}")
        else:
            self.breadcrumb_label.setText(f"ARKITECH PORTAL  /  {title.upper()}")

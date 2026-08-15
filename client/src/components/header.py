from PySide6.QtWidgets import QWidget, QHBoxLayout, QVBoxLayout, QLabel, QPushButton, QFrame
from PySide6.QtCore import Qt, Signal
from PySide6.QtGui import QCursor


class Header(QWidget):
    """Top bar component for page titles, server status badge, and refresh trigger."""

    refresh_requested = Signal()

    def __init__(self, parent=None):
        super().__init__(parent)
        self.setObjectName("Header")
        self.setStyleSheet("""
            QWidget#Header {
                background-color: #0d1322;
                border-bottom: 1px solid rgba(255, 255, 255, 0.07);
                padding: 12px 28px;
            }
        """)

        layout = QHBoxLayout(self)
        layout.setContentsMargins(24, 14, 24, 14)
        layout.setSpacing(16)

        # Title & Subtitle with breadcrumb
        text_layout = QVBoxLayout()
        text_layout.setSpacing(2)

        self.breadcrumb_label = QLabel("ARKITECH PORTAL  /  PANOU PRINCIPAL")
        self.breadcrumb_label.setStyleSheet("color: #818cf8; font-size: 10px; font-weight: 700; letter-spacing: 0.8px;")
        text_layout.addWidget(self.breadcrumb_label)

        self.title_label = QLabel("Tablou de bord")
        self.title_label.setObjectName("HeaderTitle")
        self.title_label.setStyleSheet("color: #ffffff; font-size: 20px; font-weight: 800; letter-spacing: -0.3px;")
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
                background-color: rgba(16, 185, 129, 0.1);
                border: 1px solid rgba(16, 185, 129, 0.25);
                border-radius: 8px;
                padding: 6px 12px;
            }
        """)
        status_layout = QHBoxLayout(status_frame)
        status_layout.setContentsMargins(4, 2, 4, 2)
        status_layout.setSpacing(8)

        dot = QLabel("●")
        dot.setStyleSheet("color: #10b981; font-size: 11px;")
        status_layout.addWidget(dot)

        status_text = QLabel("Backend Conectat")
        status_text.setStyleSheet("color: #34d399; font-size: 11px; font-weight: 700;")
        status_layout.addWidget(status_text)
        layout.addWidget(status_frame)

        # Refresh button
        self.refresh_btn = QPushButton("🔄 Actualizează")
        self.refresh_btn.setCursor(QCursor(Qt.PointingHandCursor))
        self.refresh_btn.setStyleSheet("""
            QPushButton {
                background-color: #1e293b;
                color: #e2e8f0;
                border: 1px solid rgba(255, 255, 255, 0.1);
                border-radius: 8px;
                padding: 8px 14px;
                font-size: 12px;
                font-weight: 600;
            }
            QPushButton:hover {
                background-color: #334155;
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
            self.breadcrumb_label.setText(breadcrumb.upper())
        else:
            self.breadcrumb_label.setText(f"ARKITECH PORTAL  /  {title.upper()}")

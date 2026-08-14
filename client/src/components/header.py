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
                background-color: #0f172a;
                border-bottom: 1px solid #1e293b;
                padding: 12px 24px;
            }
        """)

        layout = QHBoxLayout(self)
        layout.setContentsMargins(20, 12, 20, 12)
        layout.setSpacing(16)

        # Title & Subtitle
        text_layout = QVBoxLayout()
        text_layout.setSpacing(2)

        self.title_label = QLabel("Panou Principal")
        self.title_label.setStyleSheet("color: #ffffff; font-size: 20px; font-weight: 700;")
        text_layout.addWidget(self.title_label)

        self.subtitle_label = QLabel("Bine ați venit în platforma educațională ArkiTech")
        self.subtitle_label.setStyleSheet("color: #64748b; font-size: 12px;")
        text_layout.addWidget(self.subtitle_label)

        layout.addLayout(text_layout)
        layout.addStretch()

        # Server status badge
        status_frame = QFrame()
        status_frame.setStyleSheet("""
            QFrame {
                background-color: rgba(16, 185, 129, 0.1);
                border: 1px solid rgba(16, 185, 129, 0.3);
                border-radius: 6px;
                padding: 4px 10px;
            }
        """)
        status_layout = QHBoxLayout(status_frame)
        status_layout.setContentsMargins(4, 2, 4, 2)
        status_layout.setSpacing(6)

        dot = QLabel("●")
        dot.setStyleSheet("color: #10b981; font-size: 10px;")
        status_layout.addWidget(dot)

        status_text = QLabel("Server Online")
        status_text.setStyleSheet("color: #34d399; font-size: 11px; font-weight: 600;")
        status_layout.addWidget(status_text)
        layout.addWidget(status_frame)

        # Refresh button
        refresh_btn = QPushButton("🔄 Reîmprospătare")
        refresh_btn.setCursor(QCursor(Qt.PointingHandCursor))
        refresh_btn.setStyleSheet("""
            QPushButton {
                background-color: #1e293b;
                color: #cbd5e1;
                border: 1px solid #334155;
                border-radius: 6px;
                padding: 6px 12px;
                font-size: 12px;
                font-weight: 500;
            }
            QPushButton:hover {
                background-color: #334155;
                color: #ffffff;
            }
        """)
        refresh_btn.clicked.connect(self.refresh_requested.emit)
        layout.addWidget(refresh_btn)

    def set_title(self, title: str, subtitle: str = ""):
        self.title_label.setText(title)
        if subtitle:
            self.subtitle_label.setText(subtitle)

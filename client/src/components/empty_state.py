from typing import Optional, Callable
from PySide6.QtWidgets import QWidget, QVBoxLayout, QLabel, QPushButton
from PySide6.QtCore import Qt
from PySide6.QtGui import QCursor


class EmptyState(QWidget):
    """Clean empty state placeholder with icon, message, and optional action button."""

    def __init__(
        self,
        icon: str = "📂",
        title: str = "Nicio înregistrare găsită",
        message: str = "Nu există date de afișat în acest moment.",
        action_text: Optional[str] = None,
        on_action: Optional[Callable] = None,
        parent=None
    ):
        super().__init__(parent)
        layout = QVBoxLayout(self)
        layout.setAlignment(Qt.AlignCenter)
        layout.setContentsMargins(32, 48, 32, 48)
        layout.setSpacing(12)

        icon_lbl = QLabel(icon)
        icon_lbl.setAlignment(Qt.AlignCenter)
        icon_lbl.setStyleSheet("font-size: 40px;")
        layout.addWidget(icon_lbl)

        title_lbl = QLabel(title)
        title_lbl.setAlignment(Qt.AlignCenter)
        title_lbl.setStyleSheet("color: #f1f5f9; font-size: 16px; font-weight: 700;")
        layout.addWidget(title_lbl)

        msg_lbl = QLabel(message)
        msg_lbl.setAlignment(Qt.AlignCenter)
        msg_lbl.setWordWrap(True)
        msg_lbl.setStyleSheet("color: #64748b; font-size: 13px; max-width: 380px;")
        layout.addWidget(msg_lbl)

        if action_text and on_action:
            btn = QPushButton(action_text)
            btn.setCursor(QCursor(Qt.PointingHandCursor))
            btn.setProperty("class", "PrimaryBtn")
            btn.setStyleSheet("""
                QPushButton {
                    background-color: #4f46e5;
                    color: #ffffff;
                    border: none;
                    border-radius: 8px;
                    padding: 8px 18px;
                    font-weight: 600;
                    margin-top: 8px;
                }
                QPushButton:hover {
                    background-color: #4338ca;
                }
            """)
            btn.clicked.connect(on_action)
            layout.addWidget(btn, alignment=Qt.AlignCenter)

from PySide6.QtWidgets import QLabel, QFrame, QGraphicsOpacityEffect, QVBoxLayout
from PySide6.QtCore import Qt, QPropertyAnimation, QTimer, QEasingCurve


class ToastNotification(QFrame):
    """Floating non-intrusive toast notification component."""

    def __init__(self, message: str, parent=None):
        super().__init__(parent)
        self.setWindowFlags(Qt.FramelessWindowHint | Qt.WindowStaysOnTopHint | Qt.Tool)
        self.setAttribute(Qt.WA_TranslucentBackground)

        layout = QVBoxLayout(self)
        layout.setContentsMargins(16, 12, 16, 12)

        self.label = QLabel(message)
        self.label.setStyleSheet("color: #ffffff; font-weight: 700; font-size: 13px;")
        self.label.setWordWrap(True)
        layout.addWidget(self.label)

        self.setStyleSheet("""
            QFrame {
                background-color: #1e1b4b;
                border: 1px solid #6366f1;
                border-radius: 10px;
            }
        """)

        self.opacity_effect = QGraphicsOpacityEffect(self)
        self.setGraphicsEffect(self.opacity_effect)

    def show_toast(self, x: int, y: int):
        self.move(x, y)
        self.show()

        self.animation = QPropertyAnimation(self.opacity_effect, b"opacity")
        self.animation.setDuration(300)
        self.animation.setStartValue(0.0)
        self.animation.setEndValue(1.0)
        self.animation.start()

        QTimer.singleShot(3000, self.hide_toast)

    def hide_toast(self):
        self.animation = QPropertyAnimation(self.opacity_effect, b"opacity")
        self.animation.setDuration(300)
        self.animation.setStartValue(1.0)
        self.animation.setEndValue(0.0)
        self.animation.finished.connect(self.deleteLater)
        self.animation.start()

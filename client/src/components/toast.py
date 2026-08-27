from PySide6.QtWidgets import QLabel, QFrame, QGraphicsOpacityEffect
from PySide6.QtCore import Qt, QPropertyAnimation, QTimer, QEasingCurve

class ToastNotification(QFrame):
    def __init__(self, message, parent=None):
        super().__init__(parent)
        self.setWindowFlags(Qt.FramelessWindowHint | Qt.WindowStaysOnTopHint | Qt.Tool)
        self.setAttribute(Qt.WA_TranslucentBackground)
        
        layout = QVBoxLayout(self)
        label = QLabel(message)
        label.setStyleSheet("color: white; font-weight: bold;")
        layout.addWidget(label)
        
        self.setStyleSheet("""
            QFrame {
                background-color: rgba(16, 185, 129, 0.9);
                border-radius: 10px;
                padding: 10px 20px;
            }
        """)
        
        self.opacity_effect = QGraphicsOpacityEffect(self)
        self.setGraphicsEffect(self.opacity_effect)
        
    def show_toast(self, x, y):
        self.move(x, y)
        self.show()
        
        self.animation = QPropertyAnimation(self.opacity_effect, b"opacity")
        self.animation.setDuration(500)
        self.animation.setStartValue(0)
        self.animation.setEndValue(1)
        self.animation.start()
        
        QTimer.singleShot(2500, self.hide_toast)
        
    def hide_toast(self):
        self.animation.setStartValue(1)
        self.animation.setEndValue(0)
        self.animation.finished.connect(self.deleteLater)
        self.animation.start()

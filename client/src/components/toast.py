from PySide6.QtWidgets import QLabel, QFrame, QGraphicsOpacityEffect, QVBoxLayout, QApplication
from PySide6.QtCore import Qt, QPropertyAnimation, QTimer, QEasingCurve, QPoint


class ToastNotification(QFrame):
    """Floating non-intrusive toast notification component."""

    STYLE_SUCCESS = ("background-color:#064e3b; border:1px solid #10b981;", "#10b981")
    STYLE_INFO = ("background-color:#1e1b4b; border:1px solid #6366f1;", "#a5b4fc")
    STYLE_ERROR = ("background-color:#450a0a; border:1px solid #ef4444;", "#fca5a5")
    STYLE_DEFAULT = ("background-color:#1e293b; border:1px solid #334155;", "#e2e8f0")

    def __init__(self, message: str, parent=None, style="default"):
        super().__init__(parent)
        self.setWindowFlags(Qt.FramelessWindowHint | Qt.WindowStaysOnTopHint | Qt.Tool)
        self.setAttribute(Qt.WA_TranslucentBackground)

        layout = QVBoxLayout(self)
        layout.setContentsMargins(16, 12, 16, 12)

        self.label = QLabel(message)
        self.label.setWordWrap(True)
        layout.addWidget(self.label)

        bg_style, text_color = {
            "success": self.STYLE_SUCCESS,
            "info": self.STYLE_INFO,
            "error": self.STYLE_ERROR,
        }.get(style, self.STYLE_DEFAULT)

        self.setStyleSheet(f"""
            QFrame {{
                {bg_style}
                border-radius: 12px;
            }}
        """)
        self.label.setStyleSheet(
            f"color: {text_color}; font-weight: 700; font-size: 13px; background: transparent; border: none;"
        )

        self.opacity_effect = QGraphicsOpacityEffect(self)
        self.setGraphicsEffect(self.opacity_effect)
        self.setMinimumWidth(280)
        self.setMaximumWidth(420)

    def show_toast(self, x: int, y: int):
        self.adjustSize()
        self.move(x, y)
        self.show()
        self.raise_()

        self.animation = QPropertyAnimation(self.opacity_effect, b"opacity")
        self.animation.setDuration(300)
        self.animation.setStartValue(0.0)
        self.animation.setEndValue(1.0)
        self.animation.start()

        QTimer.singleShot(3500, self.hide_toast)

    def hide_toast(self):
        self.animation = QPropertyAnimation(self.opacity_effect, b"opacity")
        self.animation.setDuration(400)
        self.animation.setStartValue(1.0)
        self.animation.setEndValue(0.0)
        self.animation.finished.connect(self.deleteLater)
        self.animation.start()


class ToastManager:
    """
    Utilitar global pentru afișarea toast-urilor.
    Folosit pentru notificări la Level Up, Badge deblocat etc.
    """

    _instances = []

    @staticmethod
    def _show(message: str, style: str, parent=None):
        """Afișează un toast centrat în fereastra principală sau în parent."""
        win = parent
        if win is None:
            app = QApplication.instance()
            if app:
                for w in app.topLevelWidgets():
                    if w.isVisible():
                        win = w
                        break

        toast = ToastNotification(message, parent=win, style=style)
        toast.adjustSize()

        if win:
            # Poziționare bottom-center în fereastra principală
            px = win.x() + (win.width() - toast.sizeHint().width()) // 2
            py = win.y() + win.height() - 100
        else:
            screen = QApplication.primaryScreen().availableGeometry() if QApplication.instance() else None
            if screen:
                px = screen.width() // 2 - 140
                py = screen.height() - 120
            else:
                px, py = 100, 100

        toast.show_toast(px, py)
        ToastManager._instances.append(toast)
        QTimer.singleShot(4500, lambda: ToastManager._instances.remove(toast) if toast in ToastManager._instances else None)

    @staticmethod
    def show_success(message: str, parent=None):
        """Afișează un toast verde de succes (ex: Level Up, task rezolvat)."""
        ToastManager._show(message, "success", parent=parent)

    @staticmethod
    def show_info(message: str, parent=None):
        """Afișează un toast albastru informativ (ex: insignă deblocată)."""
        ToastManager._show(message, "info", parent=parent)

    @staticmethod
    def show_error(message: str, parent=None):
        """Afișează un toast roșu de eroare."""
        ToastManager._show(message, "error", parent=parent)

    @staticmethod
    def show_default(message: str, parent=None):
        """Afișează un toast neutru."""
        ToastManager._show(message, "default", parent=parent)

from PySide6.QtWidgets import QLabel
from PySide6.QtCore import Qt


class StatusBadge(QLabel):
    """Modern semantic status badge pill (e.g. Approved, Pending, Active)."""

    STYLES = {
        "approved": {
            "bg": "rgba(16, 185, 129, 0.15)",
            "color": "#34d399",
            "border": "rgba(16, 185, 129, 0.3)",
            "icon": "✓ ",
            "text": "Aprobat"
        },
        "graded": {
            "bg": "rgba(16, 185, 129, 0.15)",
            "color": "#34d399",
            "border": "rgba(16, 185, 129, 0.3)",
            "icon": "★ ",
            "text": "Notat"
        },
        "pending": {
            "bg": "rgba(245, 158, 11, 0.15)",
            "color": "#fbbf24",
            "border": "rgba(245, 158, 11, 0.3)",
            "icon": "⏳ ",
            "text": "În Așteptare"
        },
        "active": {
            "bg": "rgba(99, 102, 241, 0.15)",
            "color": "#a5b4fc",
            "border": "rgba(99, 102, 241, 0.3)",
            "icon": "● ",
            "text": "Activ"
        },
        "enrolled": {
            "bg": "rgba(14, 165, 233, 0.15)",
            "color": "#38bdf8",
            "border": "rgba(14, 165, 233, 0.3)",
            "icon": "✓ ",
            "text": "Înscris"
        },
        "rejected": {
            "bg": "rgba(239, 68, 68, 0.15)",
            "color": "#f87171",
            "border": "rgba(239, 68, 68, 0.3)",
            "icon": "✕ ",
            "text": "Respins"
        }
    }

    def __init__(self, status_type: str = "active", custom_text: str = None, parent=None):
        super().__init__(parent)
        self.setAlignment(Qt.AlignCenter)
        self.set_status(status_type, custom_text)

    def set_status(self, status_type: str, custom_text: str = None):
        cfg = self.STYLES.get(status_type.lower(), self.STYLES["active"])
        label_text = custom_text if custom_text else f"{cfg['icon']}{cfg['text']}"
        self.setText(label_text)
        self.setStyleSheet(f"""
            QLabel {{
                background-color: {cfg['bg']};
                color: {cfg['color']};
                border: 1px solid {cfg['border']};
                border-radius: 6px;
                padding: 4px 10px;
                font-size: 11px;
                font-weight: 700;
                letter-spacing: 0.3px;
            }}
        """)

from PySide6.QtWidgets import (
    QWidget, QVBoxLayout, QPushButton, QFrame, QLabel
)
from PySide6.QtCore import Qt, Signal
from PySide6.QtGui import QCursor
from client.src.services.auth_service import auth
from client.src.styles.theme import COLORS

class Sidebar(QWidget):
    page_changed = Signal(int)
    logout_requested = Signal()

    def __init__(self, parent=None):
        super().__init__(parent)
        self.setObjectName("Sidebar")
        self.setFixedWidth(240)
        self.setStyleSheet(f"""
            QWidget#Sidebar {{
                background-color: {COLORS['input_bg']};
                border-right: 1px solid {COLORS['border']};
            }}
        """)
        
        layout = QVBoxLayout(self)
        layout.setContentsMargins(12, 20, 12, 20)
        layout.setSpacing(8)

        # Header Logo
        header = QLabel("ANEXA ACADEMY")
        header.setStyleSheet(f"font-size: 16px; font-weight: 800; color: {COLORS['text_primary']}; margin-bottom: 20px; padding-left: 10px;")
        layout.addWidget(header)

        # Nav Buttons
        self.buttons = []
        nav_items = [("📊 Tablou de bord", 0), ("📚 Cursuri", 1), ("📝 Teme", 2), ("🎯 Progres", 3), ("👥 Elevi", 6)]
        
        for name, idx in nav_items:
            btn = QPushButton(name)
            btn.setCheckable(True)
            btn.setCursor(QCursor(Qt.PointingHandCursor))
            btn.setStyleSheet(f"""
                QPushButton {{
                    text-align: left; padding: 10px 15px; background: transparent; 
                    color: {COLORS['text_muted']}; border-radius: 8px; font-weight: 600;
                }}
                QPushButton:hover {{
                    background-color: rgba(255, 255, 255, 0.03);
                    color: {COLORS['text_primary']};
                }}
                QPushButton:checked {{
                    background-color: {COLORS['bg_card']}; color: {COLORS['text_primary']};
                    border-left: 3px solid {COLORS['input_focus']};
                }}
            """)
            btn.clicked.connect(lambda checked, i=idx: self.page_changed.emit(i))
            layout.addWidget(btn)
            self.buttons.append((idx, btn))

        layout.addStretch()

        # Footer Profil
        self.profile_card = QFrame()
        self.profile_card.setStyleSheet(f"background: {COLORS['bg_card']}; border-radius: 10px; padding: 10px;")
        p_layout = QVBoxLayout(self.profile_card)
        p_layout.addWidget(QLabel("Artiom M."))
        logout_btn = QPushButton("Deconectare")
        logout_btn.clicked.connect(self.logout_requested.emit)
        p_layout.addWidget(logout_btn)
        layout.addWidget(self.profile_card)

    def set_page_visible(self, index, visible):
        for idx, btn in self.buttons:
            if idx == index:
                btn.setVisible(visible)

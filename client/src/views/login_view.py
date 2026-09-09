from PySide6.QtWidgets import (
    QWidget, QVBoxLayout, QLabel, QLineEdit, QPushButton, QFrame
)
from PySide6.QtCore import Qt, Signal
from PySide6.QtGui import QCursor
from client.src.services.auth_service import auth
from client.src.styles.theme import COLORS

class LoginView(QWidget):
    login_successful = Signal()

    def __init__(self, parent=None):
        super().__init__(parent)
        self.setObjectName("LoginView")
        
        main_layout = QVBoxLayout(self)
        main_layout.setAlignment(Qt.AlignCenter)

        # Login card container
        card = QFrame()
        card.setFixedWidth(400)
        card.setStyleSheet(f"""
            QFrame {{
                background-color: {COLORS['bg_card']};
                border: 1px solid {COLORS['border']};
                border-radius: 16px;
                padding: 40px;
            }}
        """)
        card_layout = QVBoxLayout(card)

        # Header
        title = QLabel("Bine ai revenit")
        title.setStyleSheet(f"font-size: 22px; font-weight: 800; color: {COLORS['text_primary']};")
        subtitle = QLabel("Introdu datele pentru a accesa platforma")
        subtitle.setStyleSheet(f"font-size: 13px; color: {COLORS['text_muted']}; margin-bottom: 20px;")
        card_layout.addWidget(title)
        card_layout.addWidget(subtitle)

        # Input fields
        self.email_input = QLineEdit()
        self.email_input.setPlaceholderText("Email")
        self.email_input.setFixedHeight(44)
        card_layout.addWidget(self.email_input)

        self.pwd_input = QLineEdit()
        self.pwd_input.setPlaceholderText("Parolă")
        self.pwd_input.setEchoMode(QLineEdit.Password)
        self.pwd_input.setFixedHeight(44)
        card_layout.addWidget(self.pwd_input)

        # Error label
        self.error_lbl = QLabel("")
        self.error_lbl.setStyleSheet(f"color: {COLORS['error_text']}; background: {COLORS['error_bg']}; padding: 8px; border-radius: 8px;")
        self.error_lbl.hide()
        card_layout.addWidget(self.error_lbl)

        # Login button
        self.login_btn = QPushButton("Autentificare")
        self.login_btn.setFixedHeight(44)
        self.login_btn.setCursor(QCursor(Qt.PointingHandCursor))
        self.login_btn.clicked.connect(self._handle_login)
        card_layout.addWidget(self.login_btn)

        main_layout.addWidget(card)

    def _handle_login(self):
        email = self.email_input.text().strip()
        password = self.pwd_input.text().strip()
        try:
            auth.login(email, password)
            self.login_successful.emit()
        except Exception as e:
            self.error_lbl.setText(str(e))
            self.error_lbl.show()

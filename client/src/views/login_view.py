from PySide6.QtWidgets import (
    QWidget, QVBoxLayout, QLabel, QLineEdit, QPushButton, QFrame
)
from PySide6.QtCore import Qt, Signal, QSizePolicy
from PySide6.QtGui import QCursor, QFont
import logging
from client.src.services.auth_service import auth
from client.src.styles.theme import COLORS
from client.src.components.toast import ToastManager

logger = logging.getLogger("client.login_view")

class LoginView(QWidget):
    login_successful = Signal()

    def __init__(self, parent=None):
        super().__init__(parent)
        self.setObjectName("LoginView")
        self.setSizePolicy(QSizePolicy.Expanding, QSizePolicy.Expanding)
        
        main_layout = QVBoxLayout(self)
        main_layout.setAlignment(Qt.AlignCenter)
        main_layout.setContentsMargins(40, 40, 40, 40)

        # Login card container
        card = QFrame()
        card.setFixedWidth(420)
        card.setStyleSheet(f"""
            QFrame {{
                background-color: {COLORS['bg_card']};
                border: 1px solid {COLORS['border']};
                border-radius: 16px;
                padding: 40px;
            }}
        """)
        card_layout = QVBoxLayout(card)
        card_layout.setSpacing(24)

        # Header
        title = QLabel("Bine ai revenit")
        title.setStyleSheet(f"font-size: 28px; font-weight: 800; color: {COLORS['text_primary']}; background: transparent;")
        subtitle = QLabel("Introdu datele pentru a accesa platforma")
        subtitle.setStyleSheet(f"font-size: 14px; color: {COLORS['text_muted']}; background: transparent;")
        card_layout.addWidget(title)
        card_layout.addWidget(subtitle)

        # Input fields
        self.email_input = QLineEdit()
        self.email_input.setPlaceholderText("Email")
        self.email_input.setFixedHeight(48)
        self.email_input.setSizePolicy(QSizePolicy.Expanding, QSizePolicy.Fixed)
        self.email_input.setStyleSheet(f"""
            QLineEdit {{
                background-color: {COLORS['bg_input']};
                border: 1px solid {COLORS['border']};
                border-radius: 8px;
                padding: 12px 16px;
                font-size: 14px;
                color: {COLORS['text_primary']};
            }}
            QLineEdit:focus {{
                border: 2px solid {COLORS['input_focus']};
                background-color: {COLORS['bg_window_secondary']};
            }}
        """)
        card_layout.addWidget(self.email_input)

        self.pwd_input = QLineEdit()
        self.pwd_input.setPlaceholderText("Parolă")
        self.pwd_input.setEchoMode(QLineEdit.Password)
        self.pwd_input.setFixedHeight(48)
        self.pwd_input.setSizePolicy(QSizePolicy.Expanding, QSizePolicy.Fixed)
        self.pwd_input.setStyleSheet(f"""
            QLineEdit {{
                background-color: {COLORS['bg_input']};
                border: 1px solid {COLORS['border']};
                border-radius: 8px;
                padding: 12px 16px;
                font-size: 14px;
                color: {COLORS['text_primary']};
            }}
            QLineEdit:focus {{
                border: 2px solid {COLORS['input_focus']};
                background-color: {COLORS['bg_window_secondary']};
            }}
        """)
        card_layout.addWidget(self.pwd_input)

        # Error label
        self.error_lbl = QLabel("")
        self.error_lbl.setStyleSheet(f"color: {COLORS['error_text']}; background: {COLORS['error_bg']}; padding: 12px; border-radius: 8px; background: transparent;")
        self.error_lbl.hide()
        card_layout.addWidget(self.error_lbl)

        # Login button
        self.login_btn = QPushButton("Autentificare")
        self.login_btn.setFixedHeight(48)
        self.login_btn.setSizePolicy(QSizePolicy.Expanding, QSizePolicy.Fixed)
        self.login_btn.setCursor(QCursor(Qt.PointingHandCursor))
        self.login_btn.clicked.connect(self._handle_login)
        card_layout.addWidget(self.login_btn)

        main_layout.addWidget(card)

    def _handle_login(self):
        email = self.email_input.text().strip()
        password = self.pwd_input.text().strip()

        if not email or not password:
            self.error_lbl.setText("Te rugăm să completezi toate câmpurile.")
            self.error_lbl.show()
            return

        # Disable button during login
        self.login_btn.setEnabled(False)
        self.login_btn.setText("Se conectează...")

        # Use async API call to avoid UI blocking
        from client.src.services.api_client import api
        api.post("/auth/login",
                json_data={"email": email, "password": password},
                callback=self._on_login_success,
                error_callback=self._on_login_error)

    def _on_login_success(self, response):
        try:
            auth.apply_login_response(response)
            self.login_successful.emit()
            ToastManager.show_success("Autentificare reușită!", parent=self)
        except Exception as e:
            logger.error(f"Error processing login response: {e}")
            self._on_login_error("Eroare la procesarea răspunsului")
        finally:
            self.login_btn.setEnabled(True)
            self.login_btn.setText("Autentificare")

    def _on_login_error(self, error_msg):
        logger.error(f"Login error: {error_msg}")
        self.error_lbl.setText(error_msg)
        self.error_lbl.show()
        ToastManager.show_error(f"Eroare la autentificare: {error_msg}", parent=self)
        self.login_btn.setEnabled(True)
        self.login_btn.setText("Autentificare")

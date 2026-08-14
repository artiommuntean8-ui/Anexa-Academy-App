from PySide6.QtWidgets import (
    QWidget, QVBoxLayout, QHBoxLayout, QLabel, QLineEdit, QPushButton, QFrame, QSpacerItem, QSizePolicy
)
from PySide6.QtCore import Qt, Signal
from PySide6.QtGui import QCursor
from client.src.services.auth_service import auth


class LoginView(QWidget):
    """Modern dark theme login view for ArkiTech Student Dashboard."""

    login_successful = Signal()

    def __init__(self, parent=None):
        super().__init__(parent)
        self.setObjectName("LoginView")
        self.setStyleSheet("background-color: #0b0f19;")

        main_layout = QVBoxLayout(self)
        main_layout.setAlignment(Qt.AlignCenter)

        # Login card container
        card = QFrame()
        card.setFixedWidth(420)
        card.setStyleSheet("""
            QFrame {
                background-color: #131d33;
                border: 1px solid #1e293b;
                border-radius: 16px;
                padding: 32px;
            }
        """)

        card_layout = QVBoxLayout(card)
        card_layout.setSpacing(16)

        # Header branding
        header_layout = QVBoxLayout()
        header_layout.setAlignment(Qt.AlignCenter)
        header_layout.setSpacing(4)

        icon_lbl = QLabel("🎓")
        icon_lbl.setAlignment(Qt.AlignCenter)
        icon_lbl.setStyleSheet("font-size: 36px;")
        header_layout.addWidget(icon_lbl)

        title_lbl = QLabel("Academia ArkiTech")
        title_lbl.setAlignment(Qt.AlignCenter)
        title_lbl.setStyleSheet("color: #ffffff; font-size: 22px; font-weight: 800; letter-spacing: 0.5px;")
        header_layout.addWidget(title_lbl)

        sub_lbl = QLabel("Student Dashboard Portal")
        sub_lbl.setAlignment(Qt.AlignCenter)
        sub_lbl.setStyleSheet("color: #38bdf8; font-size: 12px; font-weight: 600; letter-spacing: 1px;")
        header_layout.addWidget(sub_lbl)

        card_layout.addLayout(header_layout)
        card_layout.addSpacing(12)

        # Error notification banner
        self.error_lbl = QLabel("")
        self.error_lbl.setWordWrap(True)
        self.error_lbl.setStyleSheet("""
            background-color: rgba(239, 68, 68, 0.15);
            border: 1px solid rgba(239, 68, 68, 0.4);
            border-radius: 8px;
            color: #fca5a5;
            padding: 8px 12px;
            font-size: 12px;
        """)
        self.error_lbl.hide()
        card_layout.addWidget(self.error_lbl)

        # Email field
        email_layout = QVBoxLayout()
        email_layout.setSpacing(4)
        email_lbl = QLabel("Adresă de Email")
        email_lbl.setStyleSheet("color: #94a3b8; font-size: 12px; font-weight: 600;")
        email_layout.addWidget(email_lbl)

        self.email_input = QLineEdit()
        self.email_input.setPlaceholderText("ex: artiom.muntean@arkitech.academy")
        self.email_input.setText("artiom.muntean@arkitech.academy")  # Pre-filled for demo convenience
        self.email_input.setStyleSheet("""
            QLineEdit {
                background-color: #1e293b;
                border: 1px solid #334155;
                border-radius: 8px;
                padding: 10px 14px;
                color: #ffffff;
                font-size: 13px;
            }
            QLineEdit:focus {
                border: 1px solid #3b82f6;
            }
        """)
        email_layout.addWidget(self.email_input)
        card_layout.addLayout(email_layout)

        # Password field
        pwd_layout = QVBoxLayout()
        pwd_layout.setSpacing(4)
        pwd_lbl = QLabel("Parolă de Acces")
        pwd_lbl.setStyleSheet("color: #94a3b8; font-size: 12px; font-weight: 600;")
        pwd_layout.addWidget(pwd_lbl)

        self.pwd_input = QLineEdit()
        self.pwd_input.setEchoMode(QLineEdit.Password)
        self.pwd_input.setPlaceholderText("Introduceți parola...")
        self.pwd_input.setText("ArkiTech2026!")  # Pre-filled for demo convenience
        self.pwd_input.setStyleSheet("""
            QLineEdit {
                background-color: #1e293b;
                border: 1px solid #334155;
                border-radius: 8px;
                padding: 10px 14px;
                color: #ffffff;
                font-size: 13px;
            }
            QLineEdit:focus {
                border: 1px solid #3b82f6;
            }
        """)
        self.pwd_input.returnPressed.connect(self._handle_login)
        pwd_layout.addWidget(self.pwd_input)
        card_layout.addLayout(pwd_layout)

        card_layout.addSpacing(6)

        # Login button
        self.login_btn = QPushButton("Conectare la Cont")
        self.login_btn.setCursor(QCursor(Qt.PointingHandCursor))
        self.login_btn.setStyleSheet("""
            QPushButton {
                background-color: #2563eb;
                color: #ffffff;
                border: none;
                border-radius: 8px;
                padding: 12px;
                font-size: 14px;
                font-weight: 700;
            }
            QPushButton:hover {
                background-color: #1d4ed8;
            }
            QPushButton:pressed {
                background-color: #1e40af;
            }
        """)
        self.login_btn.clicked.connect(self._handle_login)
        card_layout.addWidget(self.login_btn)

        # Footer info
        footer_lbl = QLabel("Sistem securizat prin autentificare JWT • FastAPI Backend")
        footer_lbl.setAlignment(Qt.AlignCenter)
        footer_lbl.setStyleSheet("color: #64748b; font-size: 11px; margin-top: 8px;")
        card_layout.addWidget(footer_lbl)

        main_layout.addWidget(card)

    def _handle_login(self):
        email = self.email_input.text().strip()
        password = self.pwd_input.text().strip()

        if not email or not password:
            self._show_error("Vă rugăm să introduceți emailul și parola.")
            return

        self.error_lbl.hide()
        self.login_btn.setEnabled(False)
        self.login_btn.setText("Se verifică...")

        try:
            auth.login(email, password)
            self.login_successful.emit()
        except RuntimeError as e:
            self._show_error(str(e))
        except Exception as e:
            self._show_error(f"Eroare neașteptată: {str(e)}")
        finally:
            self.login_btn.setEnabled(True)
            self.login_btn.setText("Conectare la Cont")

    def _show_error(self, message: str):
        self.error_lbl.setText(message)
        self.error_lbl.show()

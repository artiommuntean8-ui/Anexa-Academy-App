from PySide6.QtWidgets import (
    QWidget, QVBoxLayout, QHBoxLayout, QLabel, QLineEdit, QPushButton, QFrame
)
from PySide6.QtCore import Qt, Signal
from PySide6.QtGui import QCursor
from client.src.services.auth_service import auth


class LoginView(QWidget):
    """Modern SaaS Dark Theme Login View with multi-role demo credentials."""

    login_successful = Signal()

    def __init__(self, parent=None):
        super().__init__(parent)
        self.setObjectName("LoginView")
        self.setStyleSheet("background-color: #090d16;")

        main_layout = QVBoxLayout(self)
        main_layout.setAlignment(Qt.AlignCenter)
        main_layout.setContentsMargins(20, 20, 20, 20)

        # Login card container
        card = QFrame()
        card.setFixedWidth(460)
        card.setStyleSheet("""
            QFrame {
                background-color: #111827;
                border: 1px solid rgba(255, 255, 255, 0.1);
                border-radius: 18px;
                padding: 36px 32px;
            }
        """)

        card_layout = QVBoxLayout(card)
        card_layout.setSpacing(16)

        # Branding Header
        header_layout = QVBoxLayout()
        header_layout.setAlignment(Qt.AlignCenter)
        header_layout.setSpacing(6)

        logo_box = QFrame()
        logo_box.setFixedSize(54, 54)
        logo_box.setStyleSheet("""
            QFrame {
                background: qlineargradient(x1:0, y1:0, x2:1, y2:1, stop:0 #4f46e5, stop:1 #06b6d4);
                border-radius: 14px;
            }
        """)
        lb_layout = QVBoxLayout(logo_box)
        lb_layout.setContentsMargins(0, 0, 0, 0)
        lb_layout.setAlignment(Qt.AlignCenter)
        logo_icon = QLabel("⚡")
        logo_icon.setAlignment(Qt.AlignCenter)
        logo_icon.setStyleSheet("font-size: 26px; color: #ffffff;")
        lb_layout.addWidget(logo_icon)
        header_layout.addWidget(logo_box, alignment=Qt.AlignCenter)

        title_lbl = QLabel("Academia ArkiTech")
        title_lbl.setAlignment(Qt.AlignCenter)
        title_lbl.setStyleSheet("color: #ffffff; font-size: 22px; font-weight: 800; letter-spacing: -0.3px; margin-top: 6px;")
        header_layout.addWidget(title_lbl)

        sub_lbl = QLabel("Student & Teacher Portal")
        sub_lbl.setAlignment(Qt.AlignCenter)
        sub_lbl.setStyleSheet("color: #818cf8; font-size: 11px; font-weight: 700; letter-spacing: 1.5px; text-transform: uppercase;")
        header_layout.addWidget(sub_lbl)

        card_layout.addLayout(header_layout)
        card_layout.addSpacing(4)

        # Error notification banner
        self.error_lbl = QLabel("")
        self.error_lbl.setWordWrap(True)
        self.error_lbl.setStyleSheet("""
            background-color: rgba(239, 68, 68, 0.15);
            border: 1px solid rgba(239, 68, 68, 0.4);
            border-radius: 9px;
            color: #fca5a5;
            padding: 10px 14px;
            font-size: 12px;
            font-weight: 500;
        """)
        self.error_lbl.hide()
        card_layout.addWidget(self.error_lbl)

        # Email field
        email_layout = QVBoxLayout()
        email_layout.setSpacing(6)
        email_lbl = QLabel("Email Instituțional")
        email_lbl.setStyleSheet("color: #94a3b8; font-size: 12px; font-weight: 700;")
        email_layout.addWidget(email_lbl)

        self.email_input = QLineEdit()
        self.email_input.setPlaceholderText("ex: artiom.muntean@arkitech.academy")
        self.email_input.setText("artiom.muntean@arkitech.academy")
        self.email_input.setStyleSheet("""
            QLineEdit {
                background-color: #162035;
                border: 1px solid rgba(255, 255, 255, 0.12);
                border-radius: 9px;
                padding: 12px 14px;
                color: #ffffff;
                font-size: 13px;
            }
            QLineEdit:focus {
                border: 1.5px solid #6366f1;
            }
        """)
        email_layout.addWidget(self.email_input)
        card_layout.addLayout(email_layout)

        # Password field
        pwd_layout = QVBoxLayout()
        pwd_layout.setSpacing(6)
        pwd_lbl = QLabel("Parolă de Acces")
        pwd_lbl.setStyleSheet("color: #94a3b8; font-size: 12px; font-weight: 700;")
        pwd_layout.addWidget(pwd_lbl)

        self.pwd_input = QLineEdit()
        self.pwd_input.setEchoMode(QLineEdit.Password)
        self.pwd_input.setPlaceholderText("••••••••••••")
        self.pwd_input.setText("ArkiTech2026!")
        self.pwd_input.setStyleSheet("""
            QLineEdit {
                background-color: #162035;
                border: 1px solid rgba(255, 255, 255, 0.12);
                border-radius: 9px;
                padding: 12px 14px;
                color: #ffffff;
                font-size: 13px;
            }
            QLineEdit:focus {
                border: 1.5px solid #6366f1;
            }
        """)
        self.pwd_input.returnPressed.connect(self._handle_login)
        pwd_layout.addWidget(self.pwd_input)
        card_layout.addLayout(pwd_layout)

        card_layout.addSpacing(4)

        # Login button
        self.login_btn = QPushButton("Autentificare în Cont")
        self.login_btn.setCursor(QCursor(Qt.PointingHandCursor))
        self.login_btn.setStyleSheet("""
            QPushButton {
                background-color: #4f46e5;
                color: #ffffff;
                border: 1px solid #6366f1;
                border-radius: 9px;
                padding: 12px;
                font-size: 14px;
                font-weight: 700;
            }
            QPushButton:hover {
                background-color: #4338ca;
            }
            QPushButton:pressed {
                background-color: #3730a3;
            }
        """)
        self.login_btn.clicked.connect(self._handle_login)
        card_layout.addWidget(self.login_btn)

        # Quick demo fill helper chips
        demo_header = QLabel("⚡ CONTURI DEMO RAPIDE:")
        demo_header.setStyleSheet("color: #64748b; font-size: 10px; font-weight: 800; letter-spacing: 0.8px; margin-top: 4px;")
        card_layout.addWidget(demo_header)

        demo_row = QHBoxLayout()
        demo_row.setSpacing(6)

        btn_student = QPushButton("👨‍🎓 Student ArkiTech")
        btn_student.setCursor(QCursor(Qt.PointingHandCursor))
        btn_student.setStyleSheet("""
            QPushButton {
                background-color: rgba(99, 102, 241, 0.12);
                color: #a5b4fc;
                border: 1px solid rgba(99, 102, 241, 0.3);
                border-radius: 7px;
                padding: 6px 8px;
                font-size: 11px;
                font-weight: 600;
            }
            QPushButton:hover { background-color: rgba(99, 102, 241, 0.25); color: #ffffff; }
        """)
        btn_student.clicked.connect(lambda: self._set_credentials("artiom.muntean@arkitech.academy", "ArkiTech2026!"))
        demo_row.addWidget(btn_student)

        btn_prof = QPushButton("👨‍🏫 Profesor Ana")
        btn_prof.setCursor(QCursor(Qt.PointingHandCursor))
        btn_prof.setStyleSheet("""
            QPushButton {
                background-color: rgba(6, 182, 212, 0.12);
                color: #67e8f9;
                border: 1px solid rgba(6, 182, 212, 0.3);
                border-radius: 7px;
                padding: 6px 8px;
                font-size: 11px;
                font-weight: 600;
            }
            QPushButton:hover { background-color: rgba(6, 182, 212, 0.25); color: #ffffff; }
        """)
        btn_prof.clicked.connect(lambda: self._set_credentials("prof.an@pythonkids.ro", "Prof2026!"))
        demo_row.addWidget(btn_prof)

        btn_elev = QPushButton("👦 Elev Andrei")
        btn_elev.setCursor(QCursor(Qt.PointingHandCursor))
        btn_elev.setStyleSheet("""
            QPushButton {
                background-color: rgba(16, 185, 129, 0.12);
                color: #6ee7b7;
                border: 1px solid rgba(16, 185, 129, 0.3);
                border-radius: 7px;
                padding: 6px 8px;
                font-size: 11px;
                font-weight: 600;
            }
            QPushButton:hover { background-color: rgba(16, 185, 129, 0.25); color: #ffffff; }
        """)
        btn_elev.clicked.connect(lambda: self._set_credentials("andrei@pythonkids.ro", "Elev2026!"))
        demo_row.addWidget(btn_elev)

        card_layout.addLayout(demo_row)

        # Footer
        footer_lbl = QLabel("ArkiTech Academic Security Protocol • JWT v1")
        footer_lbl.setAlignment(Qt.AlignCenter)
        footer_lbl.setStyleSheet("color: #475569; font-size: 11px; margin-top: 4px;")
        card_layout.addWidget(footer_lbl)

        main_layout.addWidget(card)

    def _set_credentials(self, email: str, pwd: str):
        self.email_input.setText(email)
        self.pwd_input.setText(pwd)
        self.error_lbl.hide()

    def _handle_login(self):
        email = self.email_input.text().strip()
        password = self.pwd_input.text().strip()

        if not email or not password:
            self._show_error("Vă rugăm să completați atât emailul, cât și parola.")
            return

        self.error_lbl.hide()
        self.login_btn.setEnabled(False)
        self.login_btn.setText("Se verifică credențialele...")

        try:
            auth.login(email, password)
            self.login_successful.emit()
        except RuntimeError as e:
            self._show_error(str(e))
        except Exception as e:
            self._show_error(f"Eroare neprevăzută: {str(e)}")
        finally:
            self.login_btn.setEnabled(True)
            self.login_btn.setText("Autentificare în Cont")

    def _show_error(self, message: str):
        self.error_lbl.setText(message)
        self.error_lbl.show()

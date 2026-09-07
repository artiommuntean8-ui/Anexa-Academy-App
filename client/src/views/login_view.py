from PySide6.QtWidgets import (
    QWidget, QVBoxLayout, QHBoxLayout, QLabel, QLineEdit, QPushButton, QFrame, QSpacerItem, QSizePolicy
)
from PySide6.QtCore import Qt, Signal
from PySide6.QtGui import QCursor
from client.src.services.auth_service import auth


class LoginView(QWidget):
    """World-class split-screen SaaS login experience for ArkiTech Student Dashboard."""

    login_successful = Signal()

    def __init__(self, parent=None):
        super().__init__(parent)
        self.setObjectName("LoginView")
        self.setStyleSheet("background-color: #060910;")

        root_layout = QHBoxLayout(self)
        root_layout.setContentsMargins(0, 0, 0, 0)
        root_layout.setSpacing(0)

        # =========================================================================
        # LEFT SHOWCASE PANEL (Branding, Features & Live Preview)
        # =========================================================================
        left_panel = QFrame()
        left_panel.setStyleSheet("""
            QFrame {
                background: qlineargradient(x1:0, y1:0, x2:1, y2:1, stop:0 #0d102b, stop:0.4 #15113d, stop:0.8 #0b152d, stop:1 #060910);
                border-right: 1px solid rgba(255, 255, 255, 0.08);
            }
        """)
        left_layout = QVBoxLayout(left_panel)
        left_layout.setContentsMargins(48, 48, 48, 48)
        left_layout.setSpacing(24)

        # Brand header
        brand_row = QHBoxLayout()
        brand_row.setSpacing(12)

        logo_box = QFrame()
        logo_box.setFixedSize(44, 44)
        logo_box.setStyleSheet("""
            QFrame {
                background: qlineargradient(x1:0, y1:0, x2:1, y2:1, stop:0 #4f46e5, stop:1 #06b6d4);
                border-radius: 12px;
                border: 1px solid rgba(255, 255, 255, 0.2);
            }
        """)
        lb_layout = QVBoxLayout(logo_box)
        lb_layout.setContentsMargins(0, 0, 0, 0)
        lb_layout.setAlignment(Qt.AlignCenter)
        logo_icon = QLabel("⚡")
        logo_icon.setAlignment(Qt.AlignCenter)
        logo_icon.setStyleSheet("font-size: 22px; color: #ffffff;")
        lb_layout.addWidget(logo_icon)
        brand_row.addWidget(logo_box)

        brand_text = QVBoxLayout()
        brand_text.setSpacing(1)
        b_title = QLabel("ARKITECH ACADEMY")
        b_title.setStyleSheet("color: #ffffff; font-size: 16px; font-weight: 900; letter-spacing: 1px;")
        b_sub = QLabel("NEXT-GEN LEARNING PLATFORM")
        b_sub.setStyleSheet("color: #818cf8; font-size: 9px; font-weight: 800; letter-spacing: 1.5px;")
        brand_text.addWidget(b_title)
        brand_text.addWidget(b_sub)
        brand_row.addLayout(brand_text)
        brand_row.addStretch()
        left_layout.addLayout(brand_row)

        left_layout.addSpacing(16)

        # Hero Title & Subtitle
        hero_title = QLabel("Învață Programare\nla Standard Enterprise.")
        hero_title.setStyleSheet("color: #ffffff; font-size: 30px; font-weight: 900; letter-spacing: -0.5px; line-height: 1.2;")
        left_layout.addWidget(hero_title)

        hero_desc = QLabel("Platformă educațională interactivă cu verificare automată a codului, teste unitare în timp real și sistem de gamificare.")
        hero_desc.setWordWrap(True)
        hero_desc.setStyleSheet("color: #94a3b8; font-size: 14px; line-height: 1.5;")
        left_layout.addWidget(hero_desc)

        left_layout.addSpacing(12)

        # Feature Highlights Cards
        features = [
            ("⚡", "Auto-Grader AI & Teste Unitare", "Evaluare automată a codului în milisecunde cu indicii pedagogice."),
            ("🎮", "Gamificare & Puncte XP", "Niveluri academice, ranguri și insigne deblocabile la fiecare succes."),
            ("📊", "Panou de Monitorizare Live", "Sincronizare în timp real între elevi, profesori și catalogul de note.")
        ]

        for icon_str, f_title, f_desc in features:
            f_frame = QFrame()
            f_frame.setStyleSheet("""
                QFrame {
                    background-color: rgba(255, 255, 255, 0.03);
                    border: 1px solid rgba(255, 255, 255, 0.06);
                    border-radius: 12px;
                    padding: 12px 14px;
                }
            """)
            f_layout = QHBoxLayout(f_frame)
            f_layout.setSpacing(14)

            ic_lbl = QLabel(icon_str)
            ic_lbl.setStyleSheet("font-size: 22px;")
            f_layout.addWidget(ic_lbl)

            f_txt = QVBoxLayout()
            f_txt.setSpacing(2)
            t = QLabel(f_title)
            t.setStyleSheet("color: #ffffff; font-size: 13px; font-weight: 700;")
            d = QLabel(f_desc)
            d.setStyleSheet("color: #64748b; font-size: 11px;")
            d.setWordWrap(True)
            f_txt.addWidget(t)
            f_txt.addWidget(d)
            f_layout.addLayout(f_txt)
            left_layout.addWidget(f_frame)

        left_layout.addStretch()

        # Mini Code Preview Box
        code_box = QFrame()
        code_box.setStyleSheet("""
            QFrame {
                background-color: #070a13;
                border: 1px solid rgba(99, 102, 241, 0.25);
                border-radius: 10px;
                padding: 12px 14px;
            }
        """)
        cb_layout = QVBoxLayout(code_box)
        cb_layout.setSpacing(4)
        cb_head = QLabel("python_preview.py  •  Auto-Grader ✓ 100%")
        cb_head.setStyleSheet("color: #64748b; font-size: 10px; font-weight: 800; font-family: 'Consolas', monospace;")
        cb_layout.addWidget(cb_head)

        code_snippet = QLabel("def este_par(n):\n    return n % 2 == 0  # ✓ Teste unitare validate")
        code_snippet.setStyleSheet("color: #38bdf8; font-family: 'Consolas', monospace; font-size: 12px;")
        cb_layout.addWidget(code_snippet)
        left_layout.addWidget(code_box)

        root_layout.addWidget(left_panel, stretch=4)

        # =========================================================================
        # RIGHT LOGIN FORM PANEL
        # =========================================================================
        right_panel = QFrame()
        right_panel.setStyleSheet("background-color: #080b11;")
        right_layout = QVBoxLayout(right_panel)
        right_layout.setAlignment(Qt.AlignCenter)
        right_layout.setContentsMargins(40, 40, 40, 40)

        # Form card container
        form_card = QFrame()
        form_card.setFixedWidth(420)
        form_card.setStyleSheet("""
            QFrame {
                background-color: #0e1424;
                border: 1px solid rgba(255, 255, 255, 0.08);
                border-radius: 20px;
                padding: 32px;
            }
        """)
        card_layout = QVBoxLayout(form_card)
        card_layout.setSpacing(18)

        # Header inside form
        form_head = QVBoxLayout()
        form_head.setSpacing(4)
        form_title = QLabel("Bine ai venit!")
        form_title.setStyleSheet("color: #ffffff; font-size: 24px; font-weight: 900; letter-spacing: -0.3px;")
        form_sub = QLabel("Introdu credențialele pentru a accesa platforma.")
        form_sub.setStyleSheet("color: #94a3b8; font-size: 13px;")
        form_head.addWidget(form_title)
        form_head.addWidget(form_sub)
        card_layout.addLayout(form_head)

        # Role Selector Switcher
        role_label = QLabel("SELECTEAZĂ ROLUL:")
        role_label.setStyleSheet("color: #64748b; font-size: 10px; font-weight: 800; letter-spacing: 0.8px;")
        card_layout.addWidget(role_label)

        role_row = QHBoxLayout()
        role_row.setSpacing(6)

        self.btn_role_student = QPushButton("👨‍🎓 Student")
        self.btn_role_student.setCursor(QCursor(Qt.PointingHandCursor))
        self.btn_role_student.clicked.connect(lambda: self._set_credentials("artiom.muntean@arkitech.academy", "ArkiTech2026!"))
        role_row.addWidget(self.btn_role_student)

        self.btn_role_prof = QPushButton("👨‍🏫 Profesor")
        self.btn_role_prof.setCursor(QCursor(Qt.PointingHandCursor))
        self.btn_role_prof.clicked.connect(lambda: self._set_credentials("prof.an@pythonkids.ro", "Prof2026!"))
        role_row.addWidget(self.btn_role_prof)

        self.btn_role_elev = QPushButton("👦 Elev")
        self.btn_role_elev.setCursor(QCursor(Qt.PointingHandCursor))
        self.btn_role_elev.clicked.connect(lambda: self._set_credentials("andrei@pythonkids.ro", "Elev2026!"))
        role_row.addWidget(self.btn_role_elev)

        card_layout.addLayout(role_row)

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
            font-weight: 600;
        """)
        self.error_lbl.hide()
        card_layout.addWidget(self.error_lbl)

        # Email input field
        email_vbox = QVBoxLayout()
        email_vbox.setSpacing(6)
        email_title = QLabel("Email Instituțional")
        email_title.setStyleSheet("color: #cbd5e1; font-size: 12px; font-weight: 700;")
        email_vbox.addWidget(email_title)

        self.email_input = QLineEdit()
        self.email_input.setPlaceholderText("nume@arkitech.academy")
        self.email_input.setText("artiom.muntean@arkitech.academy")
        email_vbox.addWidget(self.email_input)
        card_layout.addLayout(email_vbox)

        # Password input field
        pwd_vbox = QVBoxLayout()
        pwd_vbox.setSpacing(6)
        pwd_title = QLabel("Parolă")
        pwd_title.setStyleSheet("color: #cbd5e1; font-size: 12px; font-weight: 700;")
        pwd_vbox.addWidget(pwd_title)

        self.pwd_input = QLineEdit()
        self.pwd_input.setEchoMode(QLineEdit.Password)
        self.pwd_input.setPlaceholderText("••••••••••••")
        self.pwd_input.setText("ArkiTech2026!")
        self.pwd_input.returnPressed.connect(self._handle_login)
        pwd_vbox.addWidget(self.pwd_input)
        card_layout.addLayout(pwd_vbox)

        card_layout.addSpacing(6)

        # Submit Login Button
        self.login_btn = QPushButton("Autentificare în Cont  ➔")
        self.login_btn.setObjectName("PrimaryButton")
        self.login_btn.setCursor(QCursor(Qt.PointingHandCursor))
        self.login_btn.setFixedHeight(46)
        self.login_btn.clicked.connect(self._handle_login)
        card_layout.addWidget(self.login_btn)

        # Security footer
        sec_lbl = QLabel("🔒 Conexiune securizată SSL • JWT Auth v1")
        sec_lbl.setAlignment(Qt.AlignCenter)
        sec_lbl.setStyleSheet("color: #475569; font-size: 11px; margin-top: 4px;")
        card_layout.addWidget(sec_lbl)

        right_layout.addWidget(form_card)
        root_layout.addWidget(right_panel, stretch=5)

    def _set_credentials(self, email: str, pwd: str):
        self.email_input.setText(email)
        self.pwd_input.setText(pwd)
        self.error_lbl.hide()

    def _handle_login(self):
        email = self.email_input.text().strip()
        password = self.pwd_input.text().strip()

        if not email or not password:
            self._show_error("Vă rugăm să introduceți atât adresa de email, cât și parola.")
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
            self.login_btn.setText("Autentificare în Cont  ➔")

    def _show_error(self, message: str):
        self.error_lbl.setText(message)
        self.error_lbl.show()

from PySide6.QtWidgets import (
    QWidget, QVBoxLayout, QHBoxLayout, QLabel, QFrame, QScrollArea, QLineEdit, QPushButton, QMessageBox
)
from PySide6.QtCore import Qt
from PySide6.QtGui import QCursor
from client.src.services.api_client import api
from client.src.services.auth_service import auth


class ProfileView(QWidget):
    """Student profile, academic identity, and security settings."""

    def __init__(self, parent=None):
        super().__init__(parent)
        self.setObjectName("ProfileView")

        outer_layout = QVBoxLayout(self)
        outer_layout.setContentsMargins(0, 0, 0, 0)

        scroll = QScrollArea()
        scroll.setWidgetResizable(True)
        scroll.setStyleSheet("QScrollArea { border: none; background-color: #0b0f19; }")

        container = QWidget()
        container.setStyleSheet("background-color: #0b0f19;")
        self.layout = QVBoxLayout(container)
        self.layout.setContentsMargins(24, 20, 24, 24)
        self.layout.setSpacing(20)

        # 1. Profile Identity Card
        self.card = QFrame()
        self.card.setStyleSheet("""
            QFrame {
                background-color: #131d33;
                border: 1px solid #1e293b;
                border-radius: 12px;
                padding: 24px;
            }
        """)
        c_layout = QVBoxLayout(self.card)
        c_layout.setSpacing(16)

        # User head
        user_top = QHBoxLayout()
        user_top.setSpacing(16)

        avatar = QLabel("👨‍🎓")
        avatar.setStyleSheet("font-size: 48px; background-color: #1e293b; border-radius: 36px; padding: 12px;")
        user_top.addWidget(avatar)

        name_layout = QVBoxLayout()
        name_layout.setSpacing(4)
        self.name_lbl = QLabel("Artiom Muntean")
        self.name_lbl.setStyleSheet("color: #ffffff; font-size: 20px; font-weight: 800;")
        self.role_badge = QLabel("STUDENT • ACADEMIA ARKITECH")
        self.role_badge.setStyleSheet("color: #38bdf8; font-size: 11px; font-weight: 700; letter-spacing: 1px;")
        name_layout.addWidget(self.name_lbl)
        name_layout.addWidget(self.role_badge)
        user_top.addLayout(name_layout)
        user_top.addStretch()

        c_layout.addLayout(user_top)

        # Details list
        self.details_layout = QVBoxLayout()
        self.details_layout.setSpacing(10)

        self.field_code = self._create_info_row("Cod Matricol Student:", "ARK-2026-001")
        self.field_email = self._create_info_row("Email Instituțional:", "artiom.muntean@arkitech.academy")
        self.field_dept = self._create_info_row("Departament / Facultate:", "Inginerie Software")
        self.field_sem = self._create_info_row("Semestru Curent:", "Semestrul 2")
        self.field_status = self._create_info_row("Stare Cont:", "Activ (Înmatriculat)")

        self.details_layout.addLayout(self.field_code)
        self.details_layout.addLayout(self.field_email)
        self.details_layout.addLayout(self.field_dept)
        self.details_layout.addLayout(self.field_sem)
        self.details_layout.addLayout(self.field_status)

        c_layout.addLayout(self.details_layout)
        self.layout.addWidget(self.card)

        # 2. Security / Password Update Frame
        sec_frame = QFrame()
        sec_frame.setStyleSheet("""
            QFrame {
                background-color: #131d33;
                border: 1px solid #1e293b;
                border-radius: 12px;
                padding: 24px;
            }
        """)
        sec_layout = QVBoxLayout(sec_frame)
        sec_layout.setSpacing(14)

        sec_title = QLabel("Securitate & Modificare Parolă")
        sec_title.setStyleSheet("color: #ffffff; font-size: 16px; font-weight: 700;")
        sec_layout.addWidget(sec_title)

        self.new_pwd_input = QLineEdit()
        self.new_pwd_input.setEchoMode(QLineEdit.Password)
        self.new_pwd_input.setPlaceholderText("Introduceți noua parolă...")
        self.new_pwd_input.setStyleSheet("""
            QLineEdit {
                background-color: #1e293b;
                border: 1px solid #334155;
                border-radius: 8px;
                padding: 10px 14px;
                color: #ffffff;
            }
        """)
        sec_layout.addWidget(self.new_pwd_input)

        update_pwd_btn = QPushButton("Actualizează Parola")
        update_pwd_btn.setCursor(QCursor(Qt.PointingHandCursor))
        update_pwd_btn.setStyleSheet("""
            QPushButton {
                background-color: #2563eb;
                color: #ffffff;
                border: none;
                border-radius: 8px;
                padding: 10px 18px;
                font-weight: 600;
                font-size: 13px;
                max-width: 180px;
            }
            QPushButton:hover {
                background-color: #1d4ed8;
            }
        """)
        update_pwd_btn.clicked.connect(self._handle_password_change)
        sec_layout.addWidget(update_pwd_btn)

        self.layout.addWidget(sec_frame)
        self.layout.addStretch()

        scroll.setWidget(container)
        outer_layout.addWidget(scroll)

    def _create_info_row(self, label: str, value: str) -> QHBoxLayout:
        layout = QHBoxLayout()
        lbl = QLabel(label)
        lbl.setStyleSheet("color: #94a3b8; font-weight: 600; font-size: 13px; min-width: 180px;")
        val = QLabel(value)
        val.setStyleSheet("color: #f8fafc; font-size: 13px; font-weight: 500;")
        layout.addWidget(lbl)
        layout.addWidget(val)
        layout.addStretch()
        return layout

    def refresh_data(self):
        user = auth.current_user
        if not user:
            return

        self.name_lbl.setText(user.get("full_name", "Student"))
        role = user.get("role", "student").upper()
        self.role_badge.setText(f"{role} • ACADEMIA ARKITECH")

        self.field_code.itemAt(1).widget().setText(user.get("student_code", "-"))
        self.field_email.itemAt(1).widget().setText(user.get("email", "-"))
        self.field_dept.itemAt(1).widget().setText(user.get("department", "Inginerie Software"))
        self.field_sem.itemAt(1).widget().setText(f"Semestrul {user.get('semester', 1)}")

    def _handle_password_change(self):
        new_pwd = self.new_pwd_input.text().strip()
        if not new_pwd:
            QMessageBox.warning(self, "Atenție", "Vă rugăm să introduceți noua parolă.")
            return

        user = auth.current_user
        if not user:
            return

        try:
            student_id = user.get("id")
            api.put(f"/students/{student_id}", json_data={"password": new_pwd})
            QMessageBox.information(self, "Succes", "Parola a fost actualizată cu succes!")
            self.new_pwd_input.clear()
        except Exception as e:
            QMessageBox.warning(self, "Eroare", f"Nu s-a putut actualiza parola: {str(e)}")

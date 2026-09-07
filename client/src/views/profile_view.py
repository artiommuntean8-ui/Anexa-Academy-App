from PySide6.QtWidgets import (
    QWidget, QVBoxLayout, QHBoxLayout, QLabel, QFrame, QScrollArea, QLineEdit, QPushButton, QMessageBox, QProgressBar
)
from PySide6.QtCore import Qt
from PySide6.QtGui import QCursor
from client.src.components.badge import StatusBadge
from client.src.services.api_client import api
from client.src.services.auth_service import auth
from client.src.config import APP_NAME, APP_VERSION, API_BASE_URL


class ProfileView(QWidget):
    """Student profile, account security, and dashboard system settings."""

    def __init__(self, parent=None):
        super().__init__(parent)
        self.setObjectName("ProfileView")

        outer_layout = QVBoxLayout(self)
        outer_layout.setContentsMargins(0, 0, 0, 0)

        scroll = QScrollArea()
        scroll.setWidgetResizable(True)
        scroll.setStyleSheet("QScrollArea { border: none; background-color: #090d16; }")

        container = QWidget()
        container.setStyleSheet("background-color: #090d16;")
        self.layout = QVBoxLayout(container)
        self.layout.setContentsMargins(28, 24, 28, 28)
        self.layout.setSpacing(24)

        # 1. Profile Identity Hero Card
        self.card = QFrame()
        self.card.setStyleSheet("""
            QFrame {
                background-color: #111827;
                border: 1px solid rgba(255, 255, 255, 0.08);
                border-radius: 16px;
                padding: 24px;
            }
        """)
        c_layout = QVBoxLayout(self.card)
        c_layout.setSpacing(20)

        # Avatar + Basic Info Row
        user_top = QHBoxLayout()
        user_top.setSpacing(16)

        self.avatar_box = QLabel("AM")
        self.avatar_box.setAlignment(Qt.AlignCenter)
        self.avatar_box.setFixedSize(60, 60)
        self.avatar_box.setStyleSheet("""
            background: qlineargradient(x1:0, y1:0, x2:1, y2:1, stop:0 #4f46e5, stop:1 #06b6d4);
            color: #ffffff;
            font-weight: 800;
            font-size: 20px;
            border-radius: 30px;
            border: 2px solid rgba(255, 255, 255, 0.2);
        """)
        user_top.addWidget(self.avatar_box)

        name_layout = QVBoxLayout()
        name_layout.setSpacing(4)
        self.name_lbl = QLabel("Artiom Muntean")
        self.name_lbl.setStyleSheet("color: #ffffff; font-size: 22px; font-weight: 800; letter-spacing: -0.3px;")
        
        role_row = QHBoxLayout()
        role_row.setSpacing(8)
        self.role_badge = StatusBadge("active", "Student Înmatriculat")
        role_row.addWidget(self.role_badge)
        
        self.academy_tag = QLabel("Academia ArkiTech")
        self.academy_tag.setStyleSheet("color: #818cf8; font-size: 12px; font-weight: 700;")
        role_row.addWidget(self.academy_tag)
        role_row.addStretch()
        
        name_layout.addWidget(self.name_lbl)
        name_layout.addLayout(role_row)
        user_top.addLayout(name_layout)
        user_top.addStretch()

        c_layout.addLayout(user_top)

        # Grid of Details
        self.details_layout = QVBoxLayout()
        self.details_layout.setSpacing(12)

        self.field_code = self._create_info_row("Cod Matricol:", "ARK-2026-001")
        self.field_email = self._create_info_row("Email Instituțional:", "artiom.muntean@arkitech.academy")
        self.field_dept = self._create_info_row("Specializare / Departament:", "Software Architecture & Engineering")
        self.field_sem = self._create_info_row("Semestrul Curent:", "Semestrul 2 (Anul I)")

        self.details_layout.addLayout(self.field_code)
        self.details_layout.addLayout(self.field_email)
        self.details_layout.addLayout(self.field_dept)
        self.details_layout.addLayout(self.field_sem)

        c_layout.addLayout(self.details_layout)
        self.layout.addWidget(self.card)

        # 2. Security & Password Card
        sec_frame = QFrame()
        sec_frame.setStyleSheet("""
            QFrame {
                background-color: #111827;
                border: 1px solid rgba(255, 255, 255, 0.08);
                border-radius: 16px;
                padding: 24px;
            }
        """)
        sec_layout = QVBoxLayout(sec_frame)
        sec_layout.setSpacing(16)

        sec_title = QLabel("Securitate Cont & Modificare Parolă")
        sec_title.setStyleSheet("color: #ffffff; font-size: 16px; font-weight: 700;")
        sec_layout.addWidget(sec_title)

        form_layout = QHBoxLayout()
        form_layout.setSpacing(16)

        self.new_pwd_input = QLineEdit()
        self.new_pwd_input.setEchoMode(QLineEdit.Password)
        self.new_pwd_input.setPlaceholderText("Introduceți noua parolă (minim 6 caractere)...")
        self.new_pwd_input.setStyleSheet("""
            QLineEdit {
                background-color: #162035;
                border: 1px solid rgba(255, 255, 255, 0.12);
                border-radius: 9px;
                padding: 10px 14px;
                color: #ffffff;
                font-size: 13px;
            }
            QLineEdit:focus {
                border-color: #6366f1;
            }
        """)
        form_layout.addWidget(self.new_pwd_input, stretch=2)

        update_pwd_btn = QPushButton("Salvează Parola")
        update_pwd_btn.setCursor(QCursor(Qt.PointingHandCursor))
        update_pwd_btn.setStyleSheet("""
            QPushButton {
                background-color: #4f46e5;
                color: #ffffff;
                border: 1px solid #6366f1;
                border-radius: 9px;
                padding: 10px 20px;
                font-weight: 700;
                font-size: 13px;
            }
            QPushButton:hover {
                background-color: #4338ca;
            }
        """)
        update_pwd_btn.clicked.connect(self._handle_password_change)
        form_layout.addWidget(update_pwd_btn)

        sec_layout.addLayout(form_layout)
        self.layout.addWidget(sec_frame)

        # 3. System Information Card
        sys_frame = QFrame()
        sys_frame.setStyleSheet("""
            QFrame {
                background-color: #111827;
                border: 1px solid rgba(255, 255, 255, 0.08);
                border-radius: 16px;
                padding: 20px 24px;
            }
        """)
        sys_layout = QVBoxLayout(sys_frame)
        sys_layout.setSpacing(10)

        sys_title = QLabel("Despre Sistemul ArkiTech Dashboard")
        sys_title.setStyleSheet("color: #ffffff; font-size: 15px; font-weight: 700;")
        sys_layout.addWidget(sys_title)

        sys_info = QLabel(f"Versiune Aplicație Desktop: v{APP_VERSION} • API Backend Endpoint: {API_BASE_URL}")
        sys_info.setStyleSheet("color: #94a3b8; font-size: 12px;")
        sys_layout.addWidget(sys_info)

        author_info = QLabel("Dezvoltat de Artiom Muntean pentru Academia ArkiTech.")
        author_info.setStyleSheet("color: #64748b; font-size: 11px;")
        sys_layout.addWidget(author_info)

        self.layout.addWidget(sys_frame)
        self.layout.addStretch()

        scroll.setWidget(container)
        outer_layout.addWidget(scroll)

    def _create_info_row(self, label: str, value: str) -> QHBoxLayout:
        layout = QHBoxLayout()
        lbl = QLabel(label)
        lbl.setStyleSheet("color: #94a3b8; font-weight: 600; font-size: 13px; min-width: 200px;")
        val = QLabel(value)
        val.setStyleSheet("color: #ffffff; font-size: 13px; font-weight: 600;")
        layout.addWidget(lbl)
        layout.addWidget(val)
        layout.addStretch()
        return layout

    def refresh_data(self):
        user = auth.current_user
        if not user:
            return

        name = user.get("full_name", "Student")
        self.name_lbl.setText(name)

        parts = name.split()
        if len(parts) >= 2:
            self.avatar_box.setText(f"{parts[0][0]}{parts[1][0]}".upper())
        elif parts:
            self.avatar_box.setText(parts[0][:2].upper())

        self.field_code.itemAt(1).widget().setText(user.get("student_code", "-"))
        self.field_email.itemAt(1).widget().setText(user.get("email", "-"))
        self.field_dept.itemAt(1).widget().setText(user.get("department", "Inginerie Software"))
        self.field_sem.itemAt(1).widget().setText(f"Semestrul {user.get('semester', 1)}")

    def _handle_password_change(self):
        new_pwd = self.new_pwd_input.text().strip()
        if len(new_pwd) < 6:
            QMessageBox.warning(self, "Atenție", "Noua parolă trebuie să conțină cel puțin 6 caractere.")
            return

        user = auth.current_user
        if not user:
            return

        try:
            student_id = user.get("id")
            api.put(f"/students/{student_id}", json_data={"password": new_pwd})
            QMessageBox.information(self, "Succes", "Parola dumneavoastră a fost actualizată cu succes!")
            self.new_pwd_input.clear()
        except Exception as e:
            QMessageBox.warning(self, "Eroare", f"Nu s-a putut actualiza parola: {str(e)}")

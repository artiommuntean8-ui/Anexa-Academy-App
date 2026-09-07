from PySide6.QtWidgets import (
    QWidget, QVBoxLayout, QHBoxLayout, QLabel, QPushButton, QButtonGroup, QFrame
)
from PySide6.QtCore import Qt, Signal
from PySide6.QtGui import QCursor
from client.src.services.auth_service import auth
from client.src.services.api_client import api


class Sidebar(QWidget):
    """Ultra-modern Obsidian SaaS sidebar navigation component."""

    page_changed = Signal(int)
    logout_requested = Signal()

    def __init__(self, parent=None):
        super().__init__(parent)
        self.setObjectName("Sidebar")
        self.setFixedWidth(270)

        self.setStyleSheet("""
            QWidget#Sidebar {
                background-color: #0a0e1a;
                border-right: 1px solid rgba(255, 255, 255, 0.07);
            }
        """)

        layout = QVBoxLayout(self)
        layout.setContentsMargins(16, 24, 16, 20)
        layout.setSpacing(10)

        # 1. Brand Logo Header
        brand_frame = QFrame()
        brand_frame.setStyleSheet("background: transparent;")
        brand_layout = QHBoxLayout(brand_frame)
        brand_layout.setContentsMargins(4, 0, 4, 0)
        brand_layout.setSpacing(12)

        logo_box = QFrame()
        logo_box.setFixedSize(38, 38)
        logo_box.setStyleSheet("""
            QFrame {
                background: qlineargradient(x1:0, y1:0, x2:1, y2:1, stop:0 #4f46e5, stop:1 #06b6d4);
                border-radius: 10px;
                border: 1px solid rgba(255, 255, 255, 0.2);
            }
        """)
        lb_layout = QVBoxLayout(logo_box)
        lb_layout.setContentsMargins(0, 0, 0, 0)
        lb_layout.setAlignment(Qt.AlignCenter)
        logo_icon = QLabel("⚡")
        logo_icon.setAlignment(Qt.AlignCenter)
        logo_icon.setStyleSheet("font-size: 19px; color: #ffffff;")
        lb_layout.addWidget(logo_icon)
        brand_layout.addWidget(logo_box)

        text_vbox = QVBoxLayout()
        text_vbox.setSpacing(1)
        brand_title = QLabel("ARKITECH")
        brand_title.setStyleSheet("color: #ffffff; font-size: 16px; font-weight: 900; letter-spacing: 0.8px;")
        
        brand_sub = QLabel("STUDENT PORTAL")
        brand_sub.setStyleSheet("color: #818cf8; font-size: 9px; font-weight: 800; letter-spacing: 1.2px;")
        
        text_vbox.addWidget(brand_title)
        text_vbox.addWidget(brand_sub)
        brand_layout.addLayout(text_vbox)
        brand_layout.addStretch()

        layout.addWidget(brand_frame)
        layout.addSpacing(16)

        # 2. Section: Navigare Principală
        nav_label = QLabel("PLATFORMĂ ACADEMICĂ")
        nav_label.setStyleSheet("color: #475569; font-size: 10px; font-weight: 800; letter-spacing: 1px; padding-left: 8px;")
        layout.addWidget(nav_label)

        self.btn_group = QButtonGroup(self)
        self.btn_group.setExclusive(True)

        self.nav_buttons = []
        nav_items = [
            ("📊  Tablou de bord", 0),
            ("📚  Catalog Cursuri", 1),
            ("📝  Teme & Proiecte", 2),
            ("🎯  Progres & Note", 3),
            ("⚙️  Setări & Profil", 4),
            ("👥  Gestionare Elevi", 5),
        ]

        for text, index in nav_items:
            btn = QPushButton(text)
            btn.setCheckable(True)
            btn.setCursor(QCursor(Qt.PointingHandCursor))
            btn.setStyleSheet("""
                QPushButton {
                    background-color: transparent;
                    color: #94a3b8;
                    border: none;
                    border-radius: 9px;
                    padding: 11px 14px;
                    text-align: left;
                    font-size: 13px;
                    font-weight: 600;
                }
                QPushButton:hover {
                    background-color: rgba(255, 255, 255, 0.04);
                    color: #f1f5f9;
                }
                QPushButton:checked {
                    background-color: rgba(99, 102, 241, 0.15);
                    color: #a5b4fc;
                    font-weight: 800;
                    border-left: 3px solid #6366f1;
                }
            """)
            self.nav_buttons.append(btn)
            self.btn_group.addButton(btn, index)
            layout.addWidget(btn)

        self.btn_group.idClicked.connect(self._on_nav_clicked)

        # Hide instructor tab by default
        self.nav_buttons[5].hide()

        if self.nav_buttons:
            self.nav_buttons[0].setChecked(True)

        layout.addStretch()

        # 3. User Profile Footer Card
        self.user_card = QFrame()
        self.user_card.setStyleSheet("""
            QFrame {
                background-color: #0e1424;
                border: 1px solid rgba(255, 255, 255, 0.07);
                border-radius: 12px;
                padding: 10px 12px;
            }
            QFrame:hover {
                border-color: rgba(99, 102, 241, 0.4);
            }
        """)
        user_layout = QHBoxLayout(self.user_card)
        user_layout.setContentsMargins(0, 0, 0, 0)
        user_layout.setSpacing(10)

        self.avatar_lbl = QLabel("AM")
        self.avatar_lbl.setAlignment(Qt.AlignCenter)
        self.avatar_lbl.setFixedSize(36, 36)
        self.avatar_lbl.setStyleSheet("""
            background: qlineargradient(x1:0, y1:0, x2:1, y2:1, stop:0 #4f46e5, stop:1 #7c3aed);
            color: #ffffff;
            font-weight: 800;
            font-size: 12px;
            border-radius: 18px;
            border: 1px solid rgba(255, 255, 255, 0.2);
        """)
        user_layout.addWidget(self.avatar_lbl)

        user_info_layout = QVBoxLayout()
        user_info_layout.setSpacing(2)
        self.user_name_lbl = QLabel("Student")
        self.user_name_lbl.setStyleSheet("color: #ffffff; font-weight: 700; font-size: 12px;")
        
        status_row = QHBoxLayout()
        status_row.setSpacing(4)
        online_dot = QLabel("●")
        online_dot.setStyleSheet("color: #10b981; font-size: 9px;")
        status_row.addWidget(online_dot)
        
        self.user_code_lbl = QLabel("Conectat")
        self.user_code_lbl.setStyleSheet("color: #64748b; font-size: 10px; font-weight: 600;")
        status_row.addWidget(self.user_code_lbl)
        status_row.addStretch()
        
        user_info_layout.addWidget(self.user_name_lbl)
        user_info_layout.addLayout(status_row)
        user_layout.addLayout(user_info_layout)
        user_layout.addStretch()

        layout.addWidget(self.user_card)

        # Logout Button
        logout_btn = QPushButton("🚪  Deconectare")
        logout_btn.setCursor(QCursor(Qt.PointingHandCursor))
        logout_btn.setStyleSheet("""
            QPushButton {
                background-color: transparent;
                color: #f87171;
                border: 1px solid rgba(239, 68, 68, 0.2);
                border-radius: 8px;
                padding: 8px 12px;
                font-size: 12px;
                font-weight: 600;
            }
            QPushButton:hover {
                background-color: rgba(239, 68, 68, 0.12);
                border-color: #ef4444;
                color: #ffffff;
            }
        """)
        logout_btn.clicked.connect(self.logout_requested.emit)
        layout.addWidget(logout_btn)

    def _on_nav_clicked(self, page_id: int):
        self.page_changed.emit(page_id)

    def set_active_index(self, index: int):
        if 0 <= index < len(self.nav_buttons):
            self.nav_buttons[index].setChecked(True)

    def set_page_visible(self, index: int, visible: bool):
        if 0 <= index < len(self.nav_buttons):
            self.nav_buttons[index].setVisible(visible)

    def update_sidebar_visibility(self):
        user = auth.current_user
        is_instructor = user and user.get("role") in ["instructor", "admin"]
        self.set_page_visible(5, is_instructor)

    def update_notifications(self):
        try:
            data = api.get("/notifications/unread-count")
            count = data.get("unread", 0)
            if count > 0:
                self.nav_buttons[2].setText(f"📝  Teme & Proiecte  ({count})")
            else:
                self.nav_buttons[2].setText("📝  Teme & Proiecte")
        except Exception:
            pass

    def update_user_info(self):
        user = auth.current_user
        if user:
            name = user.get("full_name", "Student")
            code = user.get("student_code", "")
            role = user.get("role", "student")
            self.user_name_lbl.setText(name)
            role_label = "Profesor" if role in ["instructor", "admin"] else "Student"
            self.user_code_lbl.setText(f"{code} • {role_label}" if code else role_label)

            parts = name.split()
            if len(parts) >= 2:
                initials = f"{parts[0][0]}{parts[1][0]}".upper()
            elif parts:
                initials = parts[0][:2].upper()
            else:
                initials = "ST"
            self.avatar_lbl.setText(initials)
            self.update_sidebar_visibility()

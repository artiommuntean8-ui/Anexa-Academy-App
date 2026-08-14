from typing import Callable
from PySide6.QtWidgets import (
    QWidget, QVBoxLayout, QHBoxLayout, QLabel, QPushButton, QButtonGroup, QFrame, QSpacerItem, QSizePolicy
)
from PySide6.QtCore import Qt, Signal
from PySide6.QtGui import QCursor
from client.src.services.auth_service import auth


class Sidebar(QWidget):
    """Modern dark theme sidebar navigation component."""

    page_changed = Signal(int)
    logout_requested = Signal()

    def __init__(self, parent=None):
        super().__init__(parent)
        self.setObjectName("Sidebar")
        self.setFixedWidth(260)

        self.setStyleSheet("""
            QWidget#Sidebar {
                background-color: #0f172a;
                border-right: 1px solid #1e293b;
            }
        """)

        layout = QVBoxLayout(self)
        layout.setContentsMargins(16, 24, 16, 20)
        layout.setSpacing(12)

        # Brand header
        brand_layout = QVBoxLayout()
        brand_layout.setSpacing(2)

        title_layout = QHBoxLayout()
        title_icon = QLabel("⚡")
        title_icon.setStyleSheet("font-size: 20px;")
        title_layout.addWidget(title_icon)

        brand_title = QLabel("ARKITECH")
        brand_title.setStyleSheet("color: #ffffff; font-size: 18px; font-weight: 800; letter-spacing: 1px;")
        title_layout.addWidget(brand_title)
        title_layout.addStretch()
        brand_layout.addLayout(title_layout)

        brand_sub = QLabel("STUDENT DASHBOARD")
        brand_sub.setStyleSheet("color: #38bdf8; font-size: 10px; font-weight: 700; letter-spacing: 1.5px; padding-left: 28px;")
        brand_layout.addWidget(brand_sub)

        layout.addLayout(brand_layout)
        layout.addSpacing(24)

        # Navigation section header
        nav_label = QLabel("MENIU PRINCIPAL")
        nav_label.setStyleSheet("color: #475569; font-size: 11px; font-weight: 700; letter-spacing: 1px; padding-left: 8px;")
        layout.addWidget(nav_label)

        # Button group for mutual exclusivity
        self.btn_group = QButtonGroup(self)
        self.btn_group.setExclusive(True)

        self.nav_buttons = []
        nav_items = [
            ("📊  Panou Principal", 0),
            ("📚  Cursurile Mele", 1),
            ("📝  Teme & Proiecte", 2),
            ("🎯  Note & Progres", 3),
            ("👤  Profil Student", 4),
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
                    border-radius: 8px;
                    padding: 12px 14px;
                    text-align: left;
                    font-size: 13px;
                    font-weight: 500;
                }
                QPushButton:hover {
                    background-color: #1e293b;
                    color: #ffffff;
                }
                QPushButton:checked {
                    background-color: #1e3a8a;
                    color: #60a5fa;
                    font-weight: 600;
                    border-left: 4px solid #3b82f6;
                }
            """)
            self.btn_group.addButton(btn, index)
            self.nav_buttons.append(btn)
            layout.addWidget(btn)

        self.btn_group.idClicked.connect(self._on_nav_clicked)

        # Select first button by default
        if self.nav_buttons:
            self.nav_buttons[0].setChecked(True)

        layout.addStretch()

        # Separator line
        sep = QFrame()
        sep.setFrameShape(QFrame.HLine)
        sep.setStyleSheet("color: #1e293b; background-color: #1e293b; max-height: 1px;")
        layout.addWidget(sep)

        # User profile badge card
        self.user_card = QFrame()
        self.user_card.setStyleSheet("""
            QFrame {
                background-color: #131d33;
                border: 1px solid #1e293b;
                border-radius: 8px;
                padding: 8px 10px;
            }
        """)
        user_layout = QHBoxLayout(self.user_card)
        user_layout.setContentsMargins(4, 4, 4, 4)
        user_layout.setSpacing(10)

        avatar_label = QLabel("👨‍🎓")
        avatar_label.setStyleSheet("font-size: 22px;")
        user_layout.addWidget(avatar_label)

        user_info_layout = QVBoxLayout()
        user_info_layout.setSpacing(2)
        self.user_name_lbl = QLabel("Student")
        self.user_name_lbl.setStyleSheet("color: #ffffff; font-weight: 600; font-size: 12px;")
        self.user_role_lbl = QLabel("Academia ArkiTech")
        self.user_role_lbl.setStyleSheet("color: #64748b; font-size: 10px;")
        user_info_layout.addWidget(self.user_name_lbl)
        user_info_layout.addWidget(self.user_role_lbl)
        user_layout.addLayout(user_info_layout)
        user_layout.addStretch()

        layout.addWidget(self.user_card)

        # Logout button
        logout_btn = QPushButton("🚪 Deconectare")
        logout_btn.setCursor(QCursor(Qt.PointingHandCursor))
        logout_btn.setStyleSheet("""
            QPushButton {
                background-color: transparent;
                color: #ef4444;
                border: 1px solid rgba(239, 68, 68, 0.3);
                border-radius: 8px;
                padding: 8px 12px;
                font-size: 12px;
                font-weight: 600;
            }
            QPushButton:hover {
                background-color: rgba(239, 68, 68, 0.15);
                border-color: #ef4444;
            }
        """)
        logout_btn.clicked.connect(self.logout_requested.emit)
        layout.addWidget(logout_btn)

    def _on_nav_clicked(self, page_id: int):
        self.page_changed.emit(page_id)

    def set_active_index(self, index: int):
        if 0 <= index < len(self.nav_buttons):
            self.nav_buttons[index].setChecked(True)

    def update_user_info(self):
        user = auth.current_user
        if user:
            name = user.get("full_name", "Student")
            code = user.get("student_code", "")
            self.user_name_lbl.setText(name)
            self.user_role_lbl.setText(f"{code} • Student" if code else "Student")

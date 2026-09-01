from typing import Callable
from PySide6.QtWidgets import (
    QWidget, QVBoxLayout, QHBoxLayout, QLabel, QPushButton, QButtonGroup, QFrame, QSpacerItem, QSizePolicy
)
from PySide6.QtCore import Qt, Signal
from PySide6.QtGui import QCursor
from client.src.services.auth_service import auth


class Sidebar(QWidget):
    """Modern fixed sidebar navigation component with SaaS aesthetics."""

    page_changed = Signal(int)
    logout_requested = Signal()

    def __init__(self, parent=None):
        super().__init__(parent)
        self.setObjectName("Sidebar")
        self.setFixedWidth(260)

        self.setStyleSheet("""
            QWidget#Sidebar {
                background-color: #0d1322;
                border-right: 1px solid rgba(255, 255, 255, 0.07);
            }
        """)

        layout = QVBoxLayout(self)
        layout.setContentsMargins(16, 24, 16, 20)
        layout.setSpacing(12)

        # 1. Brand header with glowing pill logo
        brand_layout = QVBoxLayout()
        brand_layout.setSpacing(3)

        title_layout = QHBoxLayout()
        title_layout.setSpacing(10)

        logo_box = QFrame()
        logo_box.setFixedSize(36, 36)
        logo_box.setStyleSheet("""
            QFrame {
                background: qlineargradient(x1:0, y1:0, x2:1, y2:1, stop:0 #4f46e5, stop:1 #06b6d4);
                border-radius: 9px;
            }
        """)
        lb_layout = QVBoxLayout(logo_box)
        lb_layout.setContentsMargins(0, 0, 0, 0)
        lb_layout.setAlignment(Qt.AlignCenter)
        logo_icon = QLabel("⚡")
        logo_icon.setAlignment(Qt.AlignCenter)
        logo_icon.setStyleSheet("font-size: 18px; color: #ffffff;")
        lb_layout.addWidget(logo_icon)
        title_layout.addWidget(logo_box)

        text_vbox = QVBoxLayout()
        text_vbox.setSpacing(0)
        brand_title = QLabel("ARKITECH")
        brand_title.setObjectName("LogoTitle")
        brand_title.setStyleSheet("color: #ffffff; font-size: 16px; font-weight: 800; letter-spacing: 0.8px;")
        
        brand_sub = QLabel("ACADEMY PORTAL")
        brand_sub.setObjectName("LogoSubtitle")
        brand_sub.setStyleSheet("color: #818cf8; font-size: 9px; font-weight: 700; letter-spacing: 1.2px;")
        
        text_vbox.addWidget(brand_title)
        text_vbox.addWidget(brand_sub)
        title_layout.addLayout(text_vbox)
        title_layout.addStretch()

        brand_layout.addLayout(title_layout)
        layout.addLayout(brand_layout)
        layout.addSpacing(20)

        # 2. Navigation Section
        nav_label = QLabel("NAVIGARE")
        nav_label.setStyleSheet("color: #475569; font-size: 10px; font-weight: 800; letter-spacing: 1.2px; padding-left: 8px;")
        layout.addWidget(nav_label)

        self.btn_group = QButtonGroup(self)
        self.btn_group.setExclusive(True)

        self.nav_buttons = []
        # As requested: [Tablou de bord / Cursuri / Teme / Progres / Setări]
        nav_items = [
            ("📊  Tablou de bord", 0),
            ("📚  Cursuri", 1),
            ("📝  Teme & Proiecte", 2),
            ("🎯  Progres & Note", 3),
            ("⚙️  Setări & Profil", 4),
        ]

            self.nav_buttons.append(btn)
            self.btn_group.addButton(btn, index)
            btn.clicked.connect(lambda checked, idx=index: self._on_nav_clicked(idx))
            layout.addWidget(btn)

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
                    padding: 12px 14px;
                    text-align: left;
                    font-size: 13px;
                    font-weight: 600;
                }
                QPushButton:hover {
                    background-color: rgba(255, 255, 255, 0.05);
                    color: #ffffff;
                }
                QPushButton:checked {
                    background-color: #1e1b4b;
                    color: #a5b4fc;
                    font-weight: 700;
                    border-left: 4px solid #6366f1;
                }
            """)
            self.btn_group.addButton(btn, index)
            self.nav_buttons.append(btn)
            layout.addWidget(btn)

        self.btn_group.idClicked.connect(self._on_nav_clicked)

        if self.nav_buttons:
            self.nav_buttons[0].setChecked(True)

        layout.addStretch()

        # 3. Separator
        sep = QFrame()
        sep.setFrameShape(QFrame.HLine)
        sep.setStyleSheet("color: rgba(255, 255, 255, 0.07); background-color: rgba(255, 255, 255, 0.07); max-height: 1px;")
        layout.addWidget(sep)

        # 4. User profile footer pill
        self.user_card = QFrame()
        self.user_card.setStyleSheet("""
            QFrame {
                background-color: #111827;
                border: 1px solid rgba(255, 255, 255, 0.08);
                border-radius: 10px;
                padding: 8px 10px;
            }
            QFrame:hover {
                border-color: rgba(99, 102, 241, 0.4);
            }
        """)
        user_layout = QHBoxLayout(self.user_card)
        user_layout.setContentsMargins(4, 4, 4, 4)
        user_layout.setSpacing(10)

        self.avatar_lbl = QLabel("AM")
        self.avatar_lbl.setAlignment(Qt.AlignCenter)
        self.avatar_lbl.setFixedSize(32, 32)
        self.avatar_lbl.setStyleSheet("""
            background: #312e81;
            color: #c7d2fe;
            font-weight: 800;
            font-size: 12px;
            border-radius: 16px;
            border: 1px solid #4338ca;
        """)
        user_layout.addWidget(self.avatar_lbl)

        user_info_layout = QVBoxLayout()
        user_info_layout.setSpacing(1)
        self.user_name_lbl = QLabel("Student")
        self.user_name_lbl.setStyleSheet("color: #ffffff; font-weight: 700; font-size: 12px;")
        self.user_code_lbl = QLabel("ARK-2026-001")
        self.user_code_lbl.setStyleSheet("color: #64748b; font-size: 10px; font-weight: 600;")
        user_info_layout.addWidget(self.user_name_lbl)
        user_info_layout.addWidget(self.user_code_lbl)
        user_layout.addLayout(user_info_layout)
        user_layout.addStretch()

        layout.addWidget(self.user_card)

        # Logout button
        logout_btn = QPushButton("🚪 Deconectare")
        logout_btn.setCursor(QCursor(Qt.PointingHandCursor))
        logout_btn.setStyleSheet("""
            QPushButton {
                background-color: transparent;
                color: #f87171;
                border: 1px solid rgba(239, 68, 68, 0.25);
                border-radius: 8px;
                padding: 8px 12px;
                font-size: 12px;
                font-weight: 600;
            }
            QPushButton:hover {
                background-color: rgba(239, 68, 68, 0.12);
                border-color: #ef4444;
                color: #ffffff;
    def set_page_visible(self, index, visible):
        if 0 <= index < len(self.nav_buttons):
            self.nav_buttons[index].setVisible(visible)

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
            self.user_code_lbl.setText(f"{code} • Student" if code else "Student")
            
            # Generate initials
            parts = name.split()
            if len(parts) >= 2:
                initials = f"{parts[0][0]}{parts[1][0]}".upper()
            elif parts:
                initials = parts[0][:2].upper()
            else:
                initials = "ST"
            self.avatar_lbl.setText(initials)

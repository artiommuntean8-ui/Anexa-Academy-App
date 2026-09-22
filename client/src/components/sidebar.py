from PySide6.QtWidgets import (
    QWidget, QVBoxLayout, QPushButton, QFrame, QLabel, QScrollArea
)
from PySide6.QtCore import Qt, Signal, QSizePolicy
from PySide6.QtGui import QCursor, QFont
import logging
from client.src.services.auth_service import auth
from client.src.styles.theme import COLORS

logger = logging.getLogger("client.sidebar")

class Sidebar(QWidget):
    page_changed = Signal(int)
    logout_requested = Signal()

    def __init__(self, parent=None):
        super().__init__(parent)
        self.setObjectName("Sidebar")
        self.setFixedWidth(260)
        self.setSizePolicy(QSizePolicy.Fixed, QSizePolicy.Expanding)
        
        # Modern sidebar styling
        self.setStyleSheet(f"""
            QWidget#Sidebar {{
                background-color: {COLORS['bg_sidebar']};
                border-right: 1px solid {COLORS['border']};
            }}
        """)
        
        layout = QVBoxLayout(self)
        layout.setContentsMargins(16, 20, 16, 20)
        layout.setSpacing(12)

        # Logo/Header Section
        header_container = QFrame()
        header_container.setStyleSheet(f"""
            QFrame {{
                background-color: transparent;
                border: none;
                padding: 8px 0;
            }}
        """)
        header_layout = QVBoxLayout(header_container)
        header_layout.setSpacing(8)
        
        # App Logo/Title
        logo_label = QLabel("ANEXA")
        logo_label.setStyleSheet(f"""
            QLabel {{
                font-size: 24px;
                font-weight: 800;
                color: {COLORS['accent']};
                background: transparent;
                padding: 0;
            }}
        """)
        logo_subtitle = QLabel("ACADEMY")
        logo_subtitle.setStyleSheet(f"""
            QLabel {{
                font-size: 12px;
                font-weight: 600;
                color: {COLORS['text_muted']};
                background: transparent;
                padding: 0;
                letter-spacing: 2px;
            }}
        """)
        
        header_layout.addWidget(logo_label)
        header_layout.addWidget(logo_subtitle)
        layout.addWidget(header_container)

        # Navigation Scroll Area
        nav_scroll = QScrollArea()
        nav_scroll.setWidgetResizable(True)
        nav_scroll.setStyleSheet(f"""
            QScrollArea {{
                border: none;
                background-color: transparent;
            }}
        """)
        
        nav_container = QWidget()
        nav_container.setStyleSheet("background-color: transparent;")
        nav_layout = QVBoxLayout(nav_container)
        nav_layout.setContentsMargins(0, 0, 0, 0)
        nav_layout.setSpacing(4)

        # Navigation Buttons
        self.buttons = []
        nav_items = [
            ("📊", "Tablou de bord", 0),
            ("📚", "Cursuri", 1),
            ("📝", "Teme", 2),
            ("🎯", "Progres", 3),
            ("👥", "Elevi", 6),
        ]
        
        for icon, name, idx in nav_items:
            btn = QPushButton(f"  {icon}  {name}")
            btn.setCheckable(True)
            btn.setCursor(QCursor(Qt.PointingHandCursor))
            btn.setSizePolicy(QSizePolicy.Expanding, QSizePolicy.Fixed)
            btn.setMinimumHeight(44)
            btn.setStyleSheet(f"""
                QPushButton {{
                    text-align: left;
                    background-color: transparent;
                    color: {COLORS['text_secondary']};
                    border: none;
                    border-radius: 8px;
                    padding: 8px 16px;
                    font-weight: 500;
                    font-size: 14px;
                }}
                QPushButton:hover {{
                    background-color: {COLORS['bg_card']};
                    color: {COLORS['text_primary']};
                }}
                QPushButton:checked {{
                    background-color: {COLORS['accent']};
                    color: {COLORS['text_primary']};
                    font-weight: 600;
                }}
                QPushButton:pressed {{
                    background-color: {COLORS['accent_pressed']};
                }}
            """)
            btn.clicked.connect(lambda checked, i=idx: self.page_changed.emit(i))
            nav_layout.addWidget(btn)
            self.buttons.append((idx, btn))

        nav_layout.addStretch()
        nav_scroll.setWidget(nav_container)
        layout.addWidget(nav_scroll)

        # Footer Profile Section
        profile_frame = QFrame()
        profile_frame.setStyleSheet(f"""
            QFrame {{
                background-color: {COLORS['bg_card']};
                border: 1px solid {COLORS['border']};
                border-radius: 12px;
                padding: 12px;
            }}
        """)
        self.p_layout = QVBoxLayout(profile_frame)
        self.p_layout.setContentsMargins(0, 0, 0, 0)
        self.p_layout.setSpacing(8)
        
        # Initial placeholder
        self.p_layout.addWidget(QLabel("Artiom M."))
        logout_btn = QPushButton("Deconectare")
        logout_btn.setCursor(QCursor(Qt.PointingHandCursor))
        logout_btn.setStyleSheet(f"""
            QPushButton {{
                background-color: transparent;
                color: {COLORS['error']};
                border: none;
                border-radius: 6px;
                padding: 6px 12px;
                font-weight: 600;
                font-size: 12px;
            }}
            QPushButton:hover {{
                background-color: {COLORS['error_bg']};
            }}
        """)
        logout_btn.clicked.connect(self.logout_requested.emit)
        self.p_layout.addWidget(logout_btn)
        layout.addWidget(profile_frame)

    def set_page_visible(self, index, visible):
        for idx, btn in self.buttons:
            if idx == index:
                btn.setVisible(visible)

    def update_notifications(self):
        try:
            # Placeholder for notifications - can be extended to fetch from API
            pass
        except Exception as e:
            logger.error(f"Error updating notifications: {e}")

    def update_user_info(self):
        try:
            user = auth.current_user
            if user:
                # Update profile card with user info
                # Clear existing widgets
                while self.p_layout.count():
                    item = self.p_layout.takeAt(0)
                    if item.widget():
                        item.widget().deleteLater()

                name_label = QLabel(user.get('full_name', 'Student'))
                name_label.setStyleSheet(f"color: {COLORS['text_primary']}; font-weight: 700; font-size: 13px; background: transparent;")
                self.p_layout.addWidget(name_label)

                logout_btn = QPushButton("Deconectare")
                logout_btn.setCursor(QCursor(Qt.PointingHandCursor))
                logout_btn.setStyleSheet(f"""
                    QPushButton {{
                        background-color: transparent;
                        color: {COLORS['error']};
                        border: none;
                        border-radius: 6px;
                        padding: 6px 12px;
                        font-weight: 600;
                        font-size: 12px;
                    }}
                    QPushButton:hover {{
                        background-color: {COLORS['error_bg']};
                    }}
                """)
                logout_btn.clicked.connect(self.logout_requested.emit)
                self.p_layout.addWidget(logout_btn)
        except Exception as e:
            logger.error(f"Error updating user info: {e}")

    def update_sidebar_visibility(self):
        try:
            user = auth.current_user
            if user:
                role = user.get('role', 'student')
                # Hide/show buttons based on role
                self.set_page_visible(6, role in ['admin', 'instructor'])  # Elevi (Students) management
        except Exception as e:
            logger.error(f"Error updating sidebar visibility: {e}")

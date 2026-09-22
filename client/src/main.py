# -*- coding: utf-8 -*-
import sys
import os
import logging

# Adăugăm rădăcina proiectului în sys.path
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..', '..')))

from PySide6.QtWidgets import (
    QApplication, QMainWindow, QWidget, QHBoxLayout, QVBoxLayout, QStackedWidget, QSizePolicy
)
from PySide6.QtCore import Qt
from PySide6.QtGui import QIcon

from client.src.config import APP_NAME, APP_VERSION
from client.src.styles.theme import DARK_THEME_QSS
from client.src.components.sidebar import Sidebar
from client.src.components.header import Header
from client.src.views.login_view import LoginView
from client.src.views.dashboard_view import DashboardView
from client.src.views.courses_view import CoursesView
from client.src.views.assignments_view import AssignmentsView
from client.src.views.grades_view import GradesView
from client.src.views.profile_view import ProfileView
from client.src.views.exercise_view import ExerciseView
from client.src.views.sandbox_view import SandboxView
from client.src.views.student_management_view import StudentManagementView
from client.src.services.auth_service import auth

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger("client.main")


class MainWindow(QMainWindow):
    NAV_METADATA = [
        ('Tablou de bord', 'Sinteza academică', 'Tablou de bord'),
        ('Catalog Cursuri', 'Cursuri disponibile', 'Cursuri'),
        ('Teme & Proiecte', 'Monitorizarea temelor', 'Teme'),
        ('Progres & Note', 'Situația notelor', 'Progres'),
        ('Setări & Profil', 'Setări cont', 'Setări'),
        ('Gestionare Elevi', 'Adaugă și monitorizează elevii', 'Elevi'),
    ]

    def __init__(self):
        super().__init__()
        self.setWindowTitle(f'{APP_NAME} - v{APP_VERSION}')
        
        # Set minimum size and responsive policies
        self.setMinimumSize(1200, 800)
        self.setSizePolicy(QSizePolicy.Expanding, QSizePolicy.Expanding)
        
        # Apply global dark theme stylesheet
        self.setStyleSheet(DARK_THEME_QSS)
        
        # Start maximized for full screen experience
        self.showMaximized()

        self.root_stack = QStackedWidget(self)
        self.root_stack.setSizePolicy(QSizePolicy.Expanding, QSizePolicy.Expanding)
        self.setCentralWidget(self.root_stack)

        self.login_view = LoginView()
        self.login_view.login_successful.connect(self._on_login_success)
        self.root_stack.addWidget(self.login_view)

        self.app_container = QWidget()
        self.app_container.setSizePolicy(QSizePolicy.Expanding, QSizePolicy.Expanding)
        app_layout = QHBoxLayout(self.app_container)
        app_layout.setContentsMargins(0, 0, 0, 0)
        app_layout.setSpacing(0)
        
        self.sidebar = Sidebar()
        self.sidebar.page_changed.connect(self._on_page_changed)
        self.sidebar.logout_requested.connect(self._on_logout)
        app_layout.addWidget(self.sidebar)

        content_area = QWidget()
        content_area.setSizePolicy(QSizePolicy.Expanding, QSizePolicy.Expanding)
        content_layout = QVBoxLayout(content_area)
        content_layout.setContentsMargins(0, 0, 0, 0)
        content_layout.setSpacing(0)
        
        self.header = Header()
        content_layout.addWidget(self.header)

        self.views_stack = QStackedWidget()
        self.views_stack.setSizePolicy(QSizePolicy.Expanding, QSizePolicy.Expanding)
        self.dashboard_view = DashboardView()
        self.courses_view = CoursesView()
        self.assignments_view = AssignmentsView()
        self.grades_view = GradesView()
        self.profile_view = ProfileView()
        self.exercise_view = ExerciseView()
        self.sandbox_view = SandboxView()
        self.students_view = StudentManagementView()

        self.views_stack.addWidget(self.dashboard_view)
        self.views_stack.addWidget(self.courses_view)
        self.views_stack.addWidget(self.assignments_view)
        self.views_stack.addWidget(self.grades_view)
        self.views_stack.addWidget(self.profile_view)
        self.views_stack.addWidget(self.exercise_view)
        self.views_stack.addWidget(self.sandbox_view)
        self.views_stack.addWidget(self.students_view)

        content_layout.addWidget(self.views_stack)
        app_layout.addWidget(content_area)
        self.root_stack.addWidget(self.app_container)

        if auth.load_session():
            self._on_login_success()
        else:
            self.root_stack.setCurrentIndex(0)
            
        self.sidebar.update_notifications()

    def _on_login_success(self):
        try:
            self.sidebar.update_user_info()
            self.sidebar.update_sidebar_visibility()
            self.root_stack.setCurrentIndex(1)
            self._on_page_changed(0)
        except Exception as e:
            logger.error(f"Error in login success handler: {e}")

    def _on_logout(self):
        try:
            auth.logout()
            self.root_stack.setCurrentIndex(0)
        except Exception as e:
            logger.error(f"Error in logout handler: {e}")

    def _on_page_changed(self, index):
        try:
            self.views_stack.setCurrentIndex(index)
        except Exception as e:
            logger.error(f"Error in page change handler: {e}")

    def show_exercise(self, data):
        try:
            self.exercise_view.exercise = data
            self.views_stack.setCurrentIndex(5)
        except Exception as e:
            logger.error(f"Error showing exercise: {e}")

def main():
    app = QApplication(sys.argv)
    window = MainWindow()
    window.show()
    sys.exit(app.exec())

if __name__ == '__main__':
    main()

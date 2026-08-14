import sys
import os

# Add root directory to sys.path to allow running directly
current_dir = os.path.dirname(os.path.abspath(__file__))
project_root = os.path.dirname(os.path.dirname(current_dir))
if project_root not in sys.path:
    sys.path.insert(0, project_root)

from PySide6.QtWidgets import (
    QApplication, QMainWindow, QWidget, QHBoxLayout, QVBoxLayout, QStackedWidget
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
from client.src.services.auth_service import auth


class MainWindow(QMainWindow):
    """Main Application Window for ArkiTech Student Dashboard."""

    def __init__(self):
        super().__init__()
        self.setWindowTitle(f"{APP_NAME} v{APP_VERSION}")
        self.resize(1180, 760)
        self.setMinimumSize(980, 640)

        # Root Stacked Widget (0: Login, 1: App Container)
        self.root_stack = QStackedWidget(self)
        self.setCentralWidget(self.root_stack)

        # 1. Login View
        self.login_view = LoginView()
        self.login_view.login_successful.connect(self._on_login_success)
        self.root_stack.addWidget(self.login_view)

        # 2. Main App Container
        self.app_container = QWidget()
        self.app_container.setObjectName("MainContainer")
        app_layout = QHBoxLayout(self.app_container)
        app_layout.setContentsMargins(0, 0, 0, 0)
        app_layout.setSpacing(0)

        # Sidebar
        self.sidebar = Sidebar()
        self.sidebar.page_changed.connect(self._on_page_changed)
        self.sidebar.logout_requested.connect(self._on_logout)
        app_layout.addWidget(self.sidebar)

        # Right Content Area (Header + Views Stack)
        content_area = QWidget()
        content_area.setStyleSheet("background-color: #0b0f19;")
        content_layout = QVBoxLayout(content_area)
        content_layout.setContentsMargins(0, 0, 0, 0)
        content_layout.setSpacing(0)

        # Header
        self.header = Header()
        self.header.refresh_requested.connect(self._refresh_current_view)
        content_layout.addWidget(self.header)

        # Views Stack
        self.views_stack = QStackedWidget()
        self.dashboard_view = DashboardView()
        self.courses_view = CoursesView()
        self.assignments_view = AssignmentsView()
        self.grades_view = GradesView()
        self.profile_view = ProfileView()

        self.views_stack.addWidget(self.dashboard_view)    # 0
        self.views_stack.addWidget(self.courses_view)      # 1
        self.views_stack.addWidget(self.assignments_view)  # 2
        self.views_stack.addWidget(self.grades_view)       # 3
        self.views_stack.addWidget(self.profile_view)      # 4

        content_layout.addWidget(self.views_stack)
        app_layout.addWidget(content_area)

        self.root_stack.addWidget(self.app_container)

        # Start at Login screen
        self.root_stack.setCurrentIndex(0)

    def _on_login_success(self):
        """Called when student logs in successfully."""
        self.sidebar.update_user_info()
        self.root_stack.setCurrentIndex(1)
        self.sidebar.set_active_index(0)
        self._on_page_changed(0)

    def _on_logout(self):
        """Called when student clicks logout."""
        auth.logout()
        self.root_stack.setCurrentIndex(0)

    def _on_page_changed(self, page_index: int):
        self.views_stack.setCurrentIndex(page_index)

        titles = [
            ("Panou Principal", "Sinteza academică și performanța semestrială"),
            ("Catalog Cursuri", "Toate cursurile disponibile și înscrieri"),
            ("Teme & Proiecte", "Gestionarea temelor de laborator și termenelor de predare"),
            ("Note & Progres", "Situația notelor obținute și feedback-ul profesorilor"),
            ("Profil Student", "Datele contului universitar și securitate"),
        ]

        if 0 <= page_index < len(titles):
            title, subtitle = titles[page_index]
            self.header.set_title(title, subtitle)

        self._refresh_current_view()

    def _refresh_current_view(self):
        current_widget = self.views_stack.currentWidget()
        if hasattr(current_widget, "refresh_data"):
            current_widget.refresh_data()


def main():
    app = QApplication(sys.argv)
    app.setStyleSheet(DARK_THEME_QSS)

    window = MainWindow()
    window.show()

    sys.exit(app.exec())


if __name__ == "__main__":
    main()

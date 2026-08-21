import sys
import os

# Add root directory to sys.path
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
from client.src.views.exercise_view import ExerciseView
from client.src.services.auth_service import auth


class MainWindow(QMainWindow):
    """Main Application Controller Window for ArkiTech Student Dashboard."""

    NAV_METADATA = [
        ("Tablou de bord", "Sinteza academică și performanța semestrială", "Tablou de bord"),
        ("Catalog Cursuri", "Toate cursurile disponibile și înscrieri active", "Cursuri"),
        ("Teme & Proiecte", "Monitorizarea temelor de laborator și a termenelor de predare", "Teme"),
        ("Progres & Note", "Situația notelor obținute și feedback-ul detaliat", "Progres"),
        ("Setări & Profil", "Datele contului universitar, securitate și preferințe", "Setări"),
    ]

    def __init__(self):
        super().__init__()
        self.setWindowTitle(f"{APP_NAME} — Academia ArkiTech (v{APP_VERSION})")
        self.resize(1220, 800)
        self.setMinimumSize(1020, 680)

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

        # Sidebar Navigation
        self.sidebar = Sidebar()
        self.sidebar.page_changed.connect(self._on_page_changed)
        self.sidebar.logout_requested.connect(self._on_logout)
        app_layout.addWidget(self.sidebar)

        # Right Content Area (Header + Dynamic Views)
        content_area = QWidget()
        content_area.setStyleSheet("background-color: #090d16;")
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
        self.exercise_view = ExerciseView()

        self.views_stack.addWidget(self.dashboard_view)    # Index 0
        self.views_stack.addWidget(self.courses_view)      # Index 1
        self.views_stack.addWidget(self.assignments_view)  # Index 2
        self.views_stack.addWidget(self.grades_view)       # Index 3
        self.views_stack.addWidget(self.profile_view)      # Index 4
        self.views_stack.addWidget(self.exercise_view)     # Index 5

        content_layout.addWidget(self.views_stack)
        app_layout.addWidget(content_area)

        self.root_stack.addWidget(self.app_container)

        # Initial screen: Login
        self.root_stack.setCurrentIndex(0)

    def _on_login_success(self):
        """Transition into authenticated dashboard upon successful login."""
        self.sidebar.update_user_info()
        self.root_stack.setCurrentIndex(1)
        self.sidebar.set_active_index(0)
        self._on_page_changed(0)

    def _on_logout(self):
        """Clear state and return to login view."""
        auth.logout()
        self.root_stack.setCurrentIndex(0)

    def _on_page_changed(self, page_index: int):
        self.views_stack.setCurrentIndex(page_index)

        if 0 <= page_index < len(self.NAV_METADATA):
            title, subtitle, breadcrumb = self.NAV_METADATA[page_index]
            self.header.set_title(title, subtitle, breadcrumb)
    def show_exercise(self, exercise_data):
        """Transition to the exercise view with specific content."""
        self.exercise_view.exercise = exercise_data
        # Update UI components in exercise_view
        self.views_stack.setCurrentIndex(5)
        self.header.set_title("Exercițiu", exercise_data.get("title", ""), "Exerciții")


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

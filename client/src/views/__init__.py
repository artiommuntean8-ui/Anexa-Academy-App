"""
Views package.
"""
from client.src.views.login_view import LoginView
from client.src.views.dashboard_view import DashboardView
from client.src.views.courses_view import CoursesView
from client.src.views.assignments_view import AssignmentsView
from client.src.views.grades_view import GradesView
from client.src.views.profile_view import ProfileView

__all__ = [
    "LoginView",
    "DashboardView",
    "CoursesView",
    "AssignmentsView",
    "GradesView",
    "ProfileView",
]

from typing import Optional, Dict, Any
from client.src.services.api_client import api


class AuthService:
    """Authentication and session state service."""

    def __init__(self):
        self._token: Optional[str] = None
        self._current_user: Optional[Dict[str, Any]] = None

    @property
    def is_authenticated(self) -> bool:
        return self._token is not None and self._current_user is not None

    @property
    def current_user(self) -> Optional[Dict[str, Any]]:
        return self._current_user

    @property
    def token(self) -> Optional[str]:
        return self._token

    def login(self, email: str, password: str) -> Dict[str, Any]:
        """Authenticate with backend and store session credentials."""
        payload = {"email": email, "password": password}
        response = api.post("/auth/login", json_data=payload)
        
        self._token = response.get("access_token")
        self._current_user = response.get("user")
        api.set_token(self._token)
        return response

    def register(
        self,
        student_code: str,
        full_name: str,
        email: str,
        password: str,
        department: str = "Software Engineering",
        semester: int = 1
    ) -> Dict[str, Any]:
        """Register a new student account and log in."""
        payload = {
            "student_code": student_code,
            "full_name": full_name,
            "email": email,
            "password": password,
            "department": department,
            "semester": semester
        }
        response = api.post("/auth/register", json_data=payload)
        self._token = response.get("access_token")
        self._current_user = response.get("user")
        api.set_token(self._token)
        return response

    def logout(self) -> None:
        """Clear user session and token."""
        self._token = None
        self._current_user = None
        api.set_token(None)

    def refresh_user_profile(self) -> Optional[Dict[str, Any]]:
        """Fetch fresh user profile from backend."""
        if not self._token:
            return None
        user_data = api.get("/auth/me")
        self._current_user = user_data
        return user_data


# Global singleton instance
auth = AuthService()

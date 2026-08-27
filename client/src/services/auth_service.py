import json
import os
from typing import Optional, Dict, Any
from client.src.services.api_client import api

SESSION_FILE = "session.json"

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
        self.save_session(self._token, self._current_user)
        return response

    def save_session(self, token, user):
        with open(SESSION_FILE, "w") as f:
            json.dump({"token": token, "user": user}, f)

    def load_session(self) -> bool:
        if os.path.exists(SESSION_FILE):
            try:
                with open(SESSION_FILE, "r") as f:
                    data = json.load(f)
                    self._token = data.get("token")
                    self._current_user = data.get("user")
                    api.set_token(self._token)
                    return True
            except:
                return False
        return False

    def logout(self) -> None:
        """Clear user session and token."""
        self._token = None
        self._current_user = None
        api.set_token(None)
        if os.path.exists(SESSION_FILE):
            os.remove(SESSION_FILE)

    def refresh_user_profile(self) -> Optional[Dict[str, Any]]:
        """Fetch fresh user profile from backend."""
        if not self._token:
            return None
        try:
            user_data = api.get("/auth/me")
            self._current_user = user_data
            return user_data
        except:
            return None

# Global singleton instance
auth = AuthService()

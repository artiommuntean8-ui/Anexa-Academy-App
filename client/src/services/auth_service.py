import json
import os
import logging
from pathlib import Path
from typing import Optional, Dict, Any
from client.src.services.api_client import api

logger = logging.getLogger("client.auth_service")

_CLIENT_ROOT = Path(__file__).resolve().parents[2]
SESSION_FILE = str(_CLIENT_ROOT / "session.json")


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

    def apply_login_response(self, response: Dict[str, Any]) -> Dict[str, Any]:
        self._token = response.get("access_token")
        self._current_user = response.get("user")
        if not self._token or not self._current_user:
            raise ValueError("Răspuns de autentificare invalid.")
        api.set_token(self._token)
        self.save_session(self._token, self._current_user)
        return response

    def login(self, email: str, password: str) -> Dict[str, Any]:
        """Authenticate with backend and store session credentials (sync, for tests)."""
        payload = {"email": email, "password": password}
        response = api.post("/auth/login", json_data=payload)
        return self.apply_login_response(response)

    def save_session(self, token, user):
        try:
            with open(SESSION_FILE, "w", encoding="utf-8") as f:
                json.dump({"token": token, "user": user}, f, ensure_ascii=False)
        except Exception as e:
            logger.error(f"Error saving session: {e}")

    def load_session(self) -> bool:
        if os.path.exists(SESSION_FILE):
            try:
                with open(SESSION_FILE, "r", encoding="utf-8") as f:
                    data = json.load(f)
                    self._token = data.get("token")
                    self._current_user = data.get("user")
                    if not self._token or not self._current_user:
                        return False
                    api.set_token(self._token)
                    return True
            except Exception as e:
                logger.error(f"Error loading session: {e}")
                return False
        return False

    def logout(self) -> None:
        """Clear user session and token."""
        try:
            self._token = None
            self._current_user = None
            api.set_token(None)
            if os.path.exists(SESSION_FILE):
                os.remove(SESSION_FILE)
        except Exception as e:
            logger.error(f"Error during logout: {e}")

    def refresh_user_profile(self) -> Optional[Dict[str, Any]]:
        """Fetch fresh user profile from backend."""
        if not self._token:
            return None
        try:
            user_data = api.get("/auth/me")
            self._current_user = user_data
            self.save_session(self._token, self._current_user)
            return user_data
        except Exception:
            return None


auth = AuthService()

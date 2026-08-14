"""
Services package.
"""
from client.src.services.api_client import api, APIClient
from client.src.services.auth_service import auth, AuthService

__all__ = ["api", "APIClient", "auth", "AuthService"]

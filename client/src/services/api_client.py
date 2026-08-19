from typing import Any, Dict, Optional
import requests
from client.src.config import API_BASE_URL, API_TIMEOUT


class APIClient:
    """Centralized HTTP client for communicating with FastAPI backend."""
    
    def __init__(self, base_url: str = API_BASE_URL):
        self.base_url = base_url.rstrip("/")
        self.session = requests.Session()
        self.token: Optional[str] = None

    def set_token(self, token: Optional[str]) -> None:
        """Set or remove the JWT authorization token in session headers."""
        self.token = token
        if token:
            self.session.headers.update({"Authorization": f"Bearer {token}"})
        else:
            self.session.headers.pop("Authorization", None)

    def _url(self, endpoint: str) -> str:
        if not endpoint.startswith("/"):
            endpoint = "/" + endpoint
        return f"{self.base_url}{endpoint}"

    def get(self, endpoint: str, params: Optional[Dict[str, Any]] = None) -> Dict[str, Any]:
        """Perform a GET request."""
        try:
            response = self.session.get(
                self._url(endpoint),
                params=params,
                timeout=API_TIMEOUT
            )
            response.raise_for_status()
            return response.json()
        except requests.exceptions.ConnectionError:
            raise RuntimeError("Nu s-a putut realiza conexiunea la serverul backend. Asigurați-vă că serverul este pornit.")
        except requests.exceptions.HTTPError as e:
            detail = self._extract_error_detail(response)
            raise RuntimeError(detail or f"Eroare HTTP ({response.status_code})")
        except Exception as e:
            raise RuntimeError(str(e))

    def post(self, endpoint: str, json_data: Optional[Dict[str, Any]] = None) -> Dict[str, Any]:
        """Perform a POST request."""
        try:
            response = self.session.post(
                self._url(endpoint),
                json=json_data,
                timeout=API_TIMEOUT
            )
            response.raise_for_status()
            if response.content:
                return response.json()
            return {}
        except requests.exceptions.ConnectionError:
            raise RuntimeError("Nu s-a putut realiza conexiunea la serverul backend. Asigurați-vă că serverul este pornit.")
        except requests.exceptions.HTTPError as e:
            detail = self._extract_error_detail(response)
            raise RuntimeError(detail or f"Eroare HTTP ({response.status_code})")
        except Exception as e:
            raise RuntimeError(str(e))

    def put(self, endpoint: str, json_data: Optional[Dict[str, Any]] = None) -> Dict[str, Any]:
        """Perform a PUT request."""
        try:
            response = self.session.put(
                self._url(endpoint),
                json=json_data,
                timeout=API_TIMEOUT
            )
            response.raise_for_status()
            return response.json() if response.content else {}
        except requests.exceptions.ConnectionError:
            raise RuntimeError("Nu s-a putut realiza conexiunea la serverul backend. Asigurați-vă că serverul este pornit.")
        except requests.exceptions.HTTPError as e:
            detail = self._extract_error_detail(response)
            raise RuntimeError(detail or f"Eroare HTTP ({response.status_code})")
        except Exception as e:
            raise RuntimeError(str(e))

    def delete(self, endpoint: str) -> None:
        """Perform a DELETE request."""
        try:
            response = self.session.delete(
                self._url(endpoint),
                timeout=API_TIMEOUT
            )
            response.raise_for_status()
        except requests.exceptions.ConnectionError:
            raise RuntimeError("Nu s-a putut realiza conexiunea la serverul backend. Asigurați-vă că serverul este pornit.")
        except requests.exceptions.HTTPError as e:
            detail = self._extract_error_detail(response)
            raise RuntimeError(detail or f"Eroare HTTP ({response.status_code})")
        except Exception as e:
            raise RuntimeError(str(e))

    def _extract_error_detail(self, response: requests.Response) -> Optional[str]:
        try:
            err = response.json()
            if isinstance(err, dict) and "detail" in err:
                return str(err["detail"])
        except Exception:
            pass
        return None


# Global singleton instance
api = APIClient()

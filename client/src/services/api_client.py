import json
import httpx
import logging
from PySide6.QtCore import QObject, Signal, QRunnable, QThreadPool
from client.src.config import API_BASE_URL, API_TIMEOUT

logger = logging.getLogger("client.api_client")


def _format_http_error(exc: Exception) -> str:
    if isinstance(exc, httpx.HTTPStatusError):
        try:
            detail = exc.response.json()
            if isinstance(detail, dict) and "detail" in detail:
                return str(detail["detail"])
        except Exception:
            pass
        return f"HTTP {exc.response.status_code}"
    return str(exc)


class WorkerSignals(QObject):
    result = Signal(object)
    error = Signal(str)


class APICallWorker(QRunnable):
    def __init__(self, method, endpoint, data=None, token=None, params=None, binary=False):
        super().__init__()
        self.method = method
        self.endpoint = endpoint
        self.data = data
        self.token = token
        self.params = params
        self.binary = binary
        self.signals = WorkerSignals()

    def run(self):
        headers = {"Authorization": f"Bearer {self.token}"} if self.token else {}
        url = f"{API_BASE_URL}{self.endpoint}"
        try:
            with httpx.Client(timeout=API_TIMEOUT) as client:
                response = client.request(
                    self.method,
                    url,
                    json=self.data,
                    params=self.params,
                    headers=headers,
                )
                response.raise_for_status()
                if self.binary or "application/pdf" in response.headers.get("content-type", ""):
                    self.signals.result.emit(response.content)
                else:
                    self.signals.result.emit(response.json() if response.content else {})
        except httpx.ConnectError as e:
            logger.error(f"Connection error to {url}: {e}")
            self.signals.error.emit("Eroare de conexiune la server. Verificați conexiunea la internet.")
        except httpx.TimeoutException as e:
            logger.error(f"Timeout error for {url}: {e}")
            self.signals.error.emit("Timpul de răspuns a expirat. Încercați din nou.")
        except httpx.HTTPStatusError as e:
            logger.error(f"HTTP error {e.response.status_code} for {url}: {e}")
            self.signals.error.emit(_format_http_error(e))
        except Exception as e:
            logger.error(f"Unexpected error in API call to {url}: {e}")
            self.signals.error.emit(_format_http_error(e))


class APIClient:
    def __init__(self):
        self.threadpool = QThreadPool()
        self.token = None

    def set_token(self, token):
        self.token = token

    def _headers(self):
        headers = {"Accept": "application/json"}
        if self.token:
            headers["Authorization"] = f"Bearer {self.token}"
        return headers

    def _request_sync(self, method, endpoint, json_data=None, params=None, binary=False):
        url = f"{API_BASE_URL}{endpoint}"
        try:
            with httpx.Client(timeout=API_TIMEOUT) as client:
                response = client.request(
                    method,
                    url,
                    json=json_data,
                    params=params,
                    headers=self._headers(),
                )
                response.raise_for_status()
                if binary or "application/pdf" in response.headers.get("content-type", ""):
                    return response.content
                return response.json() if response.content else {}
        except httpx.ConnectError as e:
            logger.error(f"Connection error to {url}: {e}")
            raise RuntimeError("Eroare de conexiune la server. Verificați conexiunea la internet.")
        except httpx.TimeoutException as e:
            logger.error(f"Timeout error for {url}: {e}")
            raise RuntimeError("Timpul de răspuns a expirat. Încercați din nou.")
        except httpx.HTTPStatusError as e:
            logger.error(f"HTTP error {e.response.status_code} for {url}: {e}")
            raise RuntimeError(_format_http_error(e))
        except Exception as e:
            logger.error(f"Unexpected error in API call to {url}: {e}")
            raise RuntimeError(_format_http_error(e))

    def _dispatch(self, method, endpoint, json_data=None, params=None, callback=None, error_callback=None, binary=False):
        if callback is not None:
            worker = APICallWorker(method, endpoint, json_data, self.token, params, binary)
            worker.signals.result.connect(callback)
            if error_callback:
                worker.signals.error.connect(error_callback)
            self.threadpool.start(worker)
            return None
        try:
            return self._request_sync(method, endpoint, json_data, params, binary)
        except Exception as e:
            if error_callback:
                error_callback(_format_http_error(e))
                return None
            raise RuntimeError(_format_http_error(e)) from e

    def post(self, endpoint, data=None, json_data=None, callback=None, error_callback=None, params=None):
        payload = json_data if json_data is not None else data
        return self._dispatch("POST", endpoint, payload, params, callback, error_callback)

    def get(self, endpoint, callback=None, error_callback=None, params=None, binary=False):
        return self._dispatch("GET", endpoint, None, params, callback, error_callback, binary)

    def put(self, endpoint, data=None, json_data=None, callback=None, error_callback=None, params=None):
        payload = json_data if json_data is not None else data
        return self._dispatch("PUT", endpoint, payload, params, callback, error_callback)


api = APIClient()

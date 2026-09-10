import httpx
from PySide6.QtCore import QObject, Signal, QRunnable, QThreadPool
from client.src.config import API_BASE_URL

class WorkerSignals(QObject):
    result = Signal(object)
    error = Signal(str)

class APICallWorker(QRunnable):
    def __init__(self, method, endpoint, data=None, token=None):
        super().__init__()
        self.method = method
        self.endpoint = endpoint
        self.data = data
        self.token = token
        self.signals = WorkerSignals()

    def run(self):
        headers = {"Authorization": f"Bearer {self.token}"} if self.token else {}
        url = f"{API_BASE_URL}{self.endpoint}"
        try:
            with httpx.Client(timeout=10.0) as client:
                response = client.request(self.method, url, json=self.data, headers=headers)
                response.raise_for_status()
                # Returnăm json() sau un dict gol dacă nu există conținut
                self.signals.result.emit(response.json() if response.content else {})
        except Exception as e:
            self.signals.error.emit(str(e))

class APIClient:
    def __init__(self):
        self.threadpool = QThreadPool()
        self.token = None

    def set_token(self, token):
        self.token = token

    def post(self, endpoint, data, callback, error_callback):
        worker = APICallWorker("POST", endpoint, data, self.token)
        worker.signals.result.connect(callback)
        worker.signals.error.connect(error_callback)
        self.threadpool.start(worker)

    def get(self, endpoint, callback, error_callback):
        worker = APICallWorker("GET", endpoint, None, self.token)
        worker.signals.result.connect(callback)
        worker.signals.error.connect(error_callback)
        self.threadpool.start(worker)

api = APIClient()

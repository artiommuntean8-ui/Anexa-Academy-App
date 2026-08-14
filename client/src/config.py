import os

# Desktop Client Configurations
APP_NAME = "ArkiTech Student Dashboard"
APP_VERSION = "1.0.0"
ORGANIZATION_NAME = "Academia ArkiTech"

# API Base URL
API_BASE_URL = os.getenv("API_BASE_URL", "http://127.0.0.1:8000/api/v1")
API_TIMEOUT = 10  # seconds

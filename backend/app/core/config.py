import os
import json
from pathlib import Path
from typing import List, Union
from dotenv import load_dotenv

# Base backend directory
BASE_DIR = Path(__file__).resolve().parent.parent.parent

# Load .env file
load_dotenv(BASE_DIR / ".env")

DEFAULT_SQLITE_PATH = f"sqlite:///{BASE_DIR / 'arkitech_dashboard.db'}"

try:
    from pydantic_settings import BaseSettings, SettingsConfigDict
    
    class Settings(BaseSettings):
        PROJECT_NAME: str = "Academy Student Dashboard API"
        VERSION: str = "1.0.0"
        API_V1_STR: str = "/api/v1"
        
        # JWT Security Settings
        SECRET_KEY: str = os.getenv("SECRET_KEY", "arkitech_super_secret_jwt_key_2026_change_in_production_xyz123")
        ALGORITHM: str = "HS256"
        ACCESS_TOKEN_EXPIRE_MINUTES: int = 60 * 24 * 7  # 7 days for desktop convenience
        
        # CORS Settings — no wildcard when allow_credentials=True
        BACKEND_CORS_ORIGINS: List[str] = [
            "http://localhost",
            "http://localhost:3000",
            "http://localhost:8000",
            "http://127.0.0.1:8000",
        ]

        # Database Settings
        DATABASE_URL: str = os.getenv("DATABASE_URL", DEFAULT_SQLITE_PATH)

        model_config = SettingsConfigDict(
            env_file=str(BASE_DIR / ".env"),
            env_file_encoding="utf-8",
            case_sensitive=True,
            extra="ignore"
        )

    settings = Settings()

except ImportError:
    from pydantic import BaseModel, Field

    class Settings(BaseModel):
        PROJECT_NAME: str = os.getenv("PROJECT_NAME", "Academy Student Dashboard API")
        VERSION: str = os.getenv("VERSION", "1.0.0")
        API_V1_STR: str = os.getenv("API_V1_STR", "/api/v1")
        
        # JWT Security Settings
        SECRET_KEY: str = os.getenv("SECRET_KEY", "arkitech_super_secret_jwt_key_2026_change_in_production_xyz123")
        ALGORITHM: str = "HS256"
        ACCESS_TOKEN_EXPIRE_MINUTES: int = 60 * 24 * 7
        
        BACKEND_CORS_ORIGINS: List[str] = Field(
            default_factory=lambda: [
                "http://localhost",
                "http://localhost:3000",
                "http://localhost:8000",
                "http://127.0.0.1:8000",
            ]
        )
        DATABASE_URL: str = os.getenv("DATABASE_URL", DEFAULT_SQLITE_PATH)

    settings = Settings()

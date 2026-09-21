"""
Application configuration settings loaded from environment variables.
Uses SQLite by default — zero setup required.
"""
from pydantic_settings import BaseSettings
from pydantic import field_validator
from typing import List
import os

# Path to SQLite database file
BASE_DIR = os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
SQLITE_DB_PATH = os.path.join(BASE_DIR, "customer_intelligence.db")


class Settings(BaseSettings):
    """Application settings with environment variable support."""

    # Application
    APP_NAME: str = "Customer Intelligence System"
    ENVIRONMENT: str = "development"
    DEBUG: bool = True
    API_V1_PREFIX: str = "/api"

    # Single-service deployment: serve the built React frontend from FastAPI
    SERVE_FRONTEND: bool = False
    FRONTEND_DIST: str = ""

    # Database - SQLite (default, no install needed)
    # Set DB_TYPE=mysql in .env to use MySQL instead
    DB_TYPE: str = "sqlite"
    DB_HOST: str = "localhost"
    DB_PORT: int = 3306
    DB_USER: str = "root"
    DB_PASSWORD: str = ""
    DB_NAME: str = "customer_intelligence"
    SQLITE_DB: str = SQLITE_DB_PATH

    @property
    def DATABASE_URL(self) -> str:
        if self.DB_TYPE == "mysql":
            return (
                f"mysql+aiomysql://{self.DB_USER}:{self.DB_PASSWORD}"
                f"@{self.DB_HOST}:{self.DB_PORT}/{self.DB_NAME}"
            )
        return f"sqlite+aiosqlite:///{self.SQLITE_DB}"

    @property
    def SYNC_DATABASE_URL(self) -> str:
        if self.DB_TYPE == "mysql":
            return (
                f"mysql+pymysql://{self.DB_USER}:{self.DB_PASSWORD}"
                f"@{self.DB_HOST}:{self.DB_PORT}/{self.DB_NAME}"
            )
        return f"sqlite:///{self.SQLITE_DB}"

    # JWT Authentication
    JWT_SECRET_KEY: str = "your-super-secret-key-change-in-production"
    JWT_ALGORITHM: str = "HS256"
    JWT_ACCESS_TOKEN_EXPIRE_MINUTES: int = 60
    JWT_REFRESH_TOKEN_EXPIRE_DAYS: int = 7

    # CORS (accepts comma-separated string from env or a list)
    ALLOWED_ORIGINS: List[str] = [
        "http://localhost:3000",
        "http://localhost:5173",
        "http://localhost:5174",
    ]

    @field_validator("ALLOWED_ORIGINS", mode="before")
    @classmethod
    def _parse_origins(cls, v):
        if isinstance(v, str):
            return [o.strip() for o in v.split(",") if o.strip()]
        return v

    # ML Models (absolute path so it works regardless of the process cwd)
    MODEL_DIR: str = os.path.join(BASE_DIR, "ml", "models")
    SEGMENTATION_MODEL: str = "kmeans_segmentation.pkl"
    CHURN_MODEL_RF: str = "churn_random_forest.pkl"
    CHURN_MODEL_XGB: str = "churn_xgboost.pkl"
    CHURN_MODEL_LR: str = "churn_logistic_regression.pkl"
    CLV_MODEL: str = "clv_prediction.pkl"
    SCALER_MODEL: str = "feature_scaler.pkl"

    # ML Parameters
    CHURN_THRESHOLD: float = 0.5
    NUM_CLUSTERS: int = 4
    CLV_PREDICTION_MONTHS: int = 12

    # File Upload
    UPLOAD_DIR: str = "uploads"
    MAX_UPLOAD_SIZE: int = 10 * 1024 * 1024  # 10MB

    # Reports
    REPORTS_DIR: str = "reports"

    class Config:
        env_file = ".env"
        case_sensitive = True


# Create global settings instance
settings = Settings()

# Ensure required directories exist
os.makedirs(settings.MODEL_DIR, exist_ok=True)
os.makedirs(settings.UPLOAD_DIR, exist_ok=True)
os.makedirs(settings.REPORTS_DIR, exist_ok=True)

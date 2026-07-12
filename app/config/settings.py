from functools import lru_cache

from pydantic import Field
from pydantic_settings import BaseSettings, SettingsConfigDict


class Settings(BaseSettings):
    """
    Application Settings
    Automatically loads values from .env
    """

    model_config = SettingsConfigDict(
        env_file=".env",
        env_file_encoding="utf-8",
        extra="ignore"
    )

    # ======================================================
    # Application
    # ======================================================

    app_name: str = Field(default="AI Smart Travel Planner")
    app_version: str = Field(default="1.0.0")
    environment: str = Field(default="development")
    debug: bool = Field(default=True)

    # ======================================================
    # PostgreSQL
    # ======================================================

    database_url: str

    # ======================================================
    # Google Gemini
    # ======================================================

    google_api_key: str

    # ======================================================
    # Ollama
    # ======================================================

    ollama_base_url: str
    ollama_model: str

    # ======================================================
    # Redis
    # ======================================================

    redis_url: str

    # ======================================================
    # SMTP
    # ======================================================

    smtp_email: str
    smtp_password: str

    # ======================================================
    # Razorpay
    # ======================================================

    razorpay_key_id: str
    razorpay_key_secret: str

    # ======================================================
    # JWT
    # ======================================================

    jwt_secret: str
    jwt_algorithm: str = "HS256"
    jwt_expire_minutes: int = 60

    # ======================================================
    # LangSmith
    # ======================================================

    langsmith_api_key: str | None = None
    langchain_tracing_v2: bool = False
    langchain_project: str = "AI-Smart-Travel-Planner"

    # ======================================================
    # Logging
    # ======================================================

    log_level: str = "INFO"


@lru_cache
def get_settings() -> Settings:
    """
    Returns singleton settings instance.
    """
    return Settings()


settings = get_settings()
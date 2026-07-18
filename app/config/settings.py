# app/config/settings.py
from functools import lru_cache
from pathlib import Path
from typing import Literal
from pydantic import AliasChoices, Field
from pydantic_settings import BaseSettings, SettingsConfigDict

class Settings(BaseSettings):
    model_config = SettingsConfigDict(
        env_file=".env",
        env_file_encoding="utf-8",
        extra="ignore",
    )
    
    app_name: str = "AI Smart Travel Planner"
    app_version: str = "1.0.0"
    environment: str = "development"
    debug: bool = True
    log_level: str = "INFO"
    
    # Database Configuration (Credentials removed, loaded from .env)
    database_url: str = Field(default="postgresql+psycopg://postgres:postgres@localhost:5432/travel_planner_db", validation_alias=AliasChoices("DATABASE_URL"))
    checkpoint_database_url: str = Field(default="postgresql+psycopg://postgres:postgres@localhost:5432/travel_planner_db", validation_alias=AliasChoices("CHECKPOINT_DATABASE_URL"))
    checkpointer_backend: Literal["sqlite", "postgres", "redis"] = "postgres"
    checkpointer_type: str = "postgres"
    
    # API Credentials (Secrets removed, loaded from .env)
    google_api_key: str | None = Field(default=None, validation_alias=AliasChoices("GOOGLE_API_KEY"))
    google_search_api_key: str | None = Field(default=None, validation_alias=AliasChoices("GOOGLE_SEARCH_API_KEY"))
    google_search_engine_id: str | None = Field(default=None, validation_alias=AliasChoices("GOOGLE_SEARCH_ENGINE_ID"))
    serper_api_key: str | None = Field(default=None, validation_alias=AliasChoices("SERPER_API_KEY"))
    
    # SMTP Email Configuration
    smtp_email: str | None = Field(default=None, validation_alias=AliasChoices("SMTP_EMAIL"))
    smtp_password: str | None = Field(default=None, validation_alias=AliasChoices("SMTP_PASSWORD"))
    
    # Razorpay Integration Gateway
    razorpay_key_id: str | None = Field(default=None, validation_alias=AliasChoices("RAZORPAY_KEY_ID"))
    razorpay_key_secret: str | None = Field(default=None, validation_alias=AliasChoices("RAZORPAY_KEY_SECRET"))
    demo_mode_enabled: bool = True

    @property
    def razorpay_enabled(self) -> bool:
        """Isolated feature flag ensuring app continues running if credentials are absent."""
        return bool(self.razorpay_key_id and self.razorpay_key_secret and len(self.razorpay_key_id.strip()) > 0)

    @property
    def effective_checkpoint_backend(self) -> str:
        return self.checkpointer_type or "postgres"

@lru_cache
def get_settings() -> Settings:
    return Settings()

settings = get_settings()
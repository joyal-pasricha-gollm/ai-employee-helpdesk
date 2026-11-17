"""Centralized application settings loaded from environment variables.

Values come from backend/.env (local only, never committed) or from real
environment variables. Settings are loaded lazily through get_settings() so
importing the app never fails just because a value is missing.
"""

from functools import lru_cache
from pathlib import Path

from pydantic_settings import BaseSettings, SettingsConfigDict

ENV_FILE = Path(__file__).resolve().parents[1] / ".env"

# The placeholder shipped in .env.example; it must never be used to sign tokens.
SECRET_KEY_PLACEHOLDER = "replace-with-a-random-secret-before-use"


class Settings(BaseSettings):
    """Typed application settings. Field names match the .env variable names."""

    model_config = SettingsConfigDict(
        env_file=ENV_FILE,
        env_file_encoding="utf-8",
        extra="ignore",
    )

    # Authentication (JWT)
    secret_key: str = ""
    algorithm: str = "HS256"
    access_token_expire_minutes: int = 30

    # Local AI (Ollama). Each teammate can override these in their own .env.
    ollama_base_url: str = "http://localhost:11434"
    ollama_model: str = "qwen2.5:3b"
    ollama_timeout_seconds: float = 120.0


@lru_cache
def get_settings() -> Settings:
    """Return the settings object, reading the environment only once."""
    return Settings()

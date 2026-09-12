"""Application settings loaded from the environment and an optional .env file."""

from functools import lru_cache
from typing import Literal

from pydantic_settings import BaseSettings, SettingsConfigDict


class Settings(BaseSettings):
    """Runtime configuration. Every field can be set via an IOL_MILL_* env var."""

    model_config = SettingsConfigDict(
        env_prefix="IOL_MILL_",
        env_file=".env",
        env_file_encoding="utf-8",
        extra="ignore",
    )

    app_name: str = "IOL MILL"
    environment: Literal["development", "test", "production"] = "development"
    debug: bool = False
    host: str = "0.0.0.0"
    port: int = 8000
    log_level: str = "info"
    api_prefix: str = "/api/v1"


@lru_cache
def get_settings() -> Settings:
    """Return the cached Settings instance."""
    return Settings()

from functools import lru_cache
from typing import Optional

from pydantic import AnyHttpUrl
from pydantic_settings import BaseSettings, SettingsConfigDict


class Settings(BaseSettings):
    """Configurações principais da aplicação, carregadas do ambiente (.env)."""

    model_config = SettingsConfigDict(env_file=".env", env_file_encoding="utf-8", extra="ignore")

    SPOTIFY_CLIENT_ID: str
    SPOTIFY_CLIENT_SECRET: str
    SPOTIFY_REDIRECT_URI: AnyHttpUrl

    HOST: str = "0.0.0.0"
    PORT: int = 8000
    DEBUG: bool = False

    REQUEST_TIMEOUT_SECONDS: float = 10.0
    MAX_RETRIES: int = 3

    FRONTEND_BASE_URL: Optional[AnyHttpUrl] = None


@lru_cache
def get_settings() -> Settings:
    """Retorna uma instância singleton de Settings."""

    return Settings()


settings = get_settings()


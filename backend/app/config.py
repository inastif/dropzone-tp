"""Application settings, read from environment variables (12-factor)."""

from functools import lru_cache

from pydantic_settings import BaseSettings, SettingsConfigDict


class Settings(BaseSettings):
    model_config = SettingsConfigDict(env_file=".env", extra="ignore")

    database_url: str = "sqlite:///./dropzone.db"
    log_level: str = "INFO"
    # Comma-separated list of origins allowed to call the API from a browser
    # (only needed when the front is not served behind the same domain).
    cors_origins: str = ""
    seed_demo_data: bool = True

    @property
    def cors_origin_list(self) -> list[str]:
        return [origin.strip() for origin in self.cors_origins.split(",") if origin.strip()]


@lru_cache
def get_settings() -> Settings:
    return Settings()

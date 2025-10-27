from functools import lru_cache
from pydantic import Field, SecretStr
from pydantic_settings import BaseSettings, SettingsConfigDict


class Settings(BaseSettings):
    """Runtime configuration derived from environment variables."""

    model_config = SettingsConfigDict(
        env_file=".env.local",
        env_file_encoding="utf-8",
        env_prefix="APP_",
        extra="ignore",
    )

    openai_api_key: SecretStr | None = Field(
        default=None,
        description="OpenAI API key used for GPT-4o Transcribe Diariz.",
    )
    openai_model: str = Field(
        default="gpt-4o-transcribe-diariz",
        description="Model identifier for diarized transcription.",
    )
    max_upload_minutes: int = Field(
        default=120,
        description="Maximum audio duration (minutes) accepted by the API.",
    )
    max_upload_mb: int = Field(
        default=200,
        description="Maximum audio file size in megabytes.",
    )


@lru_cache
def get_settings() -> Settings:
    """Return cached application settings."""
    return Settings()

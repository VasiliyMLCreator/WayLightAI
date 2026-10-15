from functools import lru_cache

from pydantic import Field, field_validator
from pydantic_settings import BaseSettings, SettingsConfigDict


class Settings(BaseSettings):
    yandex_api_key: str = Field(default="", validation_alias="YANDEX_API_KEY")
    yandex_folder_id: str = Field(default="", validation_alias="YANDEX_FOLDER_ID")
    yandex_model_uri: str = Field(
        default="",
        validation_alias="YANDEX_MODEL_URI",
    )
    yandex_api_url: str = Field(
        default="https://llm.api.cloud.yandex.net/foundationModels/v1/completion",
        validation_alias="YANDEX_API_URL",
    )
    max_history_messages: int = Field(default=20, validation_alias="MAX_HISTORY_MESSAGES")
    max_message_length: int = Field(default=8000, validation_alias="MAX_MESSAGE_LENGTH")
    request_timeout_seconds: float = Field(
        default=60,
        validation_alias="REQUEST_TIMEOUT_SECONDS",
    )

    model_config = SettingsConfigDict(
        env_file=".env",
        env_file_encoding="utf-8",
        extra="ignore",
    )

    @field_validator("yandex_model_uri", mode="after")
    @classmethod
    def build_model_uri(cls, value: str, info: object) -> str:
        if value:
            return value
        folder_id = info.data.get("yandex_folder_id", "")
        return f"gpt://{folder_id}/yandexgpt/latest"

    @field_validator("max_history_messages", "max_message_length")
    @classmethod
    def validate_positive(cls, value: int) -> int:
        if value < 1:
            raise ValueError("Значение должно быть положительным")
        return value


@lru_cache
def get_settings() -> Settings:
    return Settings()

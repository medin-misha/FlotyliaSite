"""
Конфигурация модуля уведомлений.

Читает переменные окружения, специфичные для этого модуля: список chat_id для
рассылки и параметры встроенного HTTP-сервера, принимающего запросы от backend.
"""

from __future__ import annotations

from pathlib import Path

from pydantic import Field, field_validator
from pydantic_settings import BaseSettings, SettingsConfigDict

BASE_DIR = Path(__file__).resolve().parent.parent.parent.parent


class NotificationsSettings(BaseSettings):
    model_config = SettingsConfigDict(
        env_file=BASE_DIR / ".env",
        env_file_encoding="utf-8",
        case_sensitive=True,
        extra="ignore",
    )

    notify_chat_ids: list[int] = Field(default_factory=list, validation_alias="NOTIFY_CHAT_IDS")
    notify_server_host: str = Field(default="0.0.0.0", validation_alias="NOTIFY_SERVER_HOST")
    notify_server_port: int = Field(default=8080, validation_alias="NOTIFY_SERVER_PORT")
    notify_secret: str | None = Field(default=None, validation_alias="NOTIFY_SECRET")

    @field_validator("notify_chat_ids", mode="before")
    @classmethod
    def parse_chat_ids(cls, v: object) -> list[int]:
        if isinstance(v, int):
            return [v]
        if isinstance(v, list):
            return [int(x) for x in v]
        if isinstance(v, str) and v.strip():
            return [int(c.strip()) for c in v.split(",") if c.strip().lstrip("-").isdigit()]
        return []


notifications_settings = NotificationsSettings()

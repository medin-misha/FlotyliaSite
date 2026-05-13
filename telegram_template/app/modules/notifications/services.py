"""
Логика отправки Telegram-уведомлений модуля notifications.

Формирует текст сообщения из данных заявки и рассылает его во все настроенные
chat_id. Ошибки отправки в один чат не блокируют остальные.
"""

from __future__ import annotations

import json
import logging
from pathlib import Path
from typing import Any

from aiogram import Bot

from .config import notifications_settings

logger = logging.getLogger(__name__)

_MESSAGES_PATH = Path(__file__).parent / "messages.json"
_MESSAGES: dict[str, str] = json.loads(_MESSAGES_PATH.read_text(encoding="utf-8"))


def _build_text(data: dict[str, Any]) -> str:
    desired = data.get("desired_transport") or ""
    how = data.get("how_found_it") or ""
    city = data.get("city") or ""

    desired_line = _MESSAGES["desired_transport_line"].format(desired_transport=desired) if desired else ""
    how_line = _MESSAGES["how_found_it_line"].format(how_found_it=how) if how else ""
    city_line = _MESSAGES["city_line"].format(city=city) if city else ""

    return _MESSAGES["new_application"].format(
        name=data.get("name") or "—",
        email=data.get("email") or "—",
        phone=data.get("phone") or "—",
        work_in=data.get("work_in") or "—",
        desired_transport_line=desired_line,
        how_found_it_line=how_line,
        city_line=city_line,
    )


async def send_application_notification(bot: Bot, data: dict[str, Any]) -> None:
    """Рассылает уведомление о новой заявке во все настроенные chat_id."""

    chat_ids = notifications_settings.notify_chat_ids
    if not chat_ids:
        logger.warning("NOTIFY_CHAT_IDS не настроен — уведомление не отправлено")
        return

    text = _build_text(data)
    for chat_id in chat_ids:
        try:
            await bot.send_message(chat_id=chat_id, text=text)
            logger.info("Уведомление о заявке отправлено в chat_id=%s", chat_id)
        except Exception as exc:
            logger.error("Не удалось отправить уведомление в chat_id=%s: %s", chat_id, exc)

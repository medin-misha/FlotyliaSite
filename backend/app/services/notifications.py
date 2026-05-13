"""
Отправка HTTP-уведомления боту при создании заявки.

Использует стандартную библиотеку urllib без дополнительных зависимостей.
Вызывается из BackgroundTasks FastAPI — не блокирует ответ пользователю.
"""

from __future__ import annotations

import asyncio
import json
import logging
from typing import Any
from urllib.error import URLError
from urllib.request import Request, urlopen

from config import settings

logger = logging.getLogger(__name__)


def _send_sync(url: str, data: dict[str, Any], secret: str | None) -> None:
    """Синхронный HTTP POST — запускается в thread executor."""

    body = json.dumps(data, ensure_ascii=False).encode("utf-8")
    headers: dict[str, str] = {"Content-Type": "application/json"}
    if secret:
        headers["X-Notify-Secret"] = secret

    req = Request(url, data=body, headers=headers, method="POST")
    try:
        with urlopen(req, timeout=5):
            pass
    except URLError as exc:
        logger.warning("Не удалось уведомить бота: %s", exc)
    except Exception as exc:
        logger.warning("Ошибка при отправке уведомления боту: %s", exc)


async def notify_new_application(data: dict[str, Any]) -> None:
    """Fire-and-forget уведомление бота о новой заявке."""

    notify_url = settings.notify_bot_url
    if not notify_url:
        return

    notify_url = notify_url.rstrip("/") + "/notify/application"
    secret = settings.notify_secret

    await asyncio.to_thread(_send_sync, notify_url, data, secret)

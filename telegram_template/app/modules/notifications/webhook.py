"""
aiohttp веб-приложение для приёма HTTP-уведомлений от backend.

Backend делает POST /notify/application с JSON-телом заявки. Если настроен
NOTIFY_SECRET, проверяется заголовок X-Notify-Secret. Боту нужна ссылка на
aiogram.Bot, чтобы отправлять сообщения — она передаётся через create_webhook_app.
"""

from __future__ import annotations

import logging
from typing import Any

from aiohttp import web
from aiogram import Bot

from .config import notifications_settings
from .services import send_application_notification

logger = logging.getLogger(__name__)


def create_webhook_app(bot: Bot) -> web.Application:
    """Собирает aiohttp-приложение с единственным эндпоинтом уведомлений."""

    app = web.Application()

    async def handle_new_application(request: web.Request) -> web.Response:
        secret = notifications_settings.notify_secret
        if secret:
            incoming = request.headers.get("X-Notify-Secret", "")
            if incoming != secret:
                logger.warning("Отклонён запрос на /notify/application: неверный секрет")
                return web.Response(status=401, text="Unauthorized")

        try:
            data: dict[str, Any] = await request.json()
        except Exception:
            return web.Response(status=400, text="Invalid JSON")

        await send_application_notification(bot, data)
        return web.Response(status=200, text="ok")

    app.router.add_post("/notify/application", handle_new_application)
    return app

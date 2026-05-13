"""
Startup/shutdown HTTP-сервера модуля уведомлений.

aiohttp-сервер запускается как фоновая задача на существующем event loop рядом
с aiogram polling. Хранит глобальный AppRunner, чтобы корректно завершиться
при остановке бота.
"""

from __future__ import annotations

import logging

from aiohttp import web
from aiogram import Bot

from .config import notifications_settings
from .webhook import create_webhook_app

logger = logging.getLogger(__name__)

_runner: web.AppRunner | None = None


async def startup_notifications_runtime(bot: Bot) -> None:
    """Запускает aiohttp-сервер уведомлений."""

    global _runner

    if _runner is not None:
        return

    aiohttp_app = create_webhook_app(bot)
    _runner = web.AppRunner(aiohttp_app)
    await _runner.setup()

    site = web.TCPSite(
        _runner,
        host=notifications_settings.notify_server_host,
        port=notifications_settings.notify_server_port,
    )
    await site.start()

    logger.info(
        "Notifications webhook server started on %s:%d",
        notifications_settings.notify_server_host,
        notifications_settings.notify_server_port,
    )


async def shutdown_notifications_runtime() -> None:
    """Останавливает aiohttp-сервер уведомлений."""

    global _runner

    if _runner is None:
        return

    await _runner.cleanup()
    _runner = None
    logger.info("Notifications webhook server stopped")

"""
Telegram-хендлеры модуля уведомлений.

Модуль работает в push-only режиме: backend вызывает HTTP-эндпоинт бота,
а тот рассылает сообщения в настроенные chat_id. Входящих Telegram-команд нет.
Router нужен для соответствия канонической структуре модуля и явной регистрации
в registry.py.
"""

from aiogram import Router

router = Router(name="notifications")

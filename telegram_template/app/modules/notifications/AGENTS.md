# Notifications Module — Agent Context

## Назначение

Push-only модуль: рассылает Telegram-уведомления о новых заявках во все chat_id
из `NOTIFY_CHAT_IDS`. Входящих Telegram-команд нет.

## Границы модуля

- `handlers.py` — пустой router, только для канонической регистрации в `registry.py`.
- `config.py` — `NotificationsSettings` с `BaseSettings`, читает собственные env-переменные.
- `services.py` — `send_application_notification(bot, data)` — единственная точка отправки.
- `webhook.py` — aiohttp app с эндпоинтом `POST /notify/application`.
- `runtime.py` — `startup_notifications_runtime(bot)` / `shutdown_notifications_runtime()`.

## Правила расширения

- Новые типы уведомлений: добавить новый эндпоинт в `webhook.py` и функцию в `services.py`.
- Изменить формат сообщения: только в `messages.json`, не трогать Python-код.
- Не добавлять auth-логику из system-модуля: этот модуль не привязан к Telegram-пользователям.
- Не добавлять FSM-состояния: модуль не ведёт диалог с пользователем.

## Интеграция с lifecycle

`runtime.py` вызывается из `app/bot/lifecycle.py`:
- `startup_notifications_runtime(bot)` — в `on_startup`
- `shutdown_notifications_runtime()` — в `on_shutdown`

## Безопасность эндпоинта

Если `NOTIFY_SECRET` задан, aiohttp проверяет заголовок `X-Notify-Secret`.
Backend должен передавать тот же секрет. Без секрета эндпоинт принимает любые
запросы — допустимо только во внутренней docker-сети.

## Что модуль не должен делать

- Не читать токен бота напрямую из `.env`.
- Не создавать отдельный aiogram Bot — использовать переданный экземпляр.
- Не хранить состояние заявок — это зона ответственности backend.

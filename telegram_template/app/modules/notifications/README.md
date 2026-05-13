# Notifications Module

`app/modules/notifications` — модуль push-уведомлений в Telegram.

Когда пользователь отправляет заявку через frontend, backend делает HTTP POST
на встроенный aiohttp-сервер бота. Модуль рассылает уведомление во все
chat_id, указанные в `NOTIFY_CHAT_IDS`.

## Как работает

1. Backend создаёт пользователя (`POST /api/v1/users/`).
2. Backend делает `POST http://telegram-bot:8080/notify/application` с JSON-телом заявки.
3. Модуль получает запрос, проверяет `X-Notify-Secret` (если настроен) и вызывает `send_application_notification`.
4. Сообщение рассылается в каждый chat_id из `NOTIFY_CHAT_IDS`.

## Переменные окружения

| Переменная | Обязательная | Пример | Описание |
|---|---|---|---|
| `NOTIFY_CHAT_IDS` | да | `123456789,-1001234567890` | Через запятую, chat_id получателей |
| `NOTIFY_SECRET` | нет | `supersecret` | Если задан — backend должен передавать его в заголовке `X-Notify-Secret` |
| `NOTIFY_SERVER_HOST` | нет | `0.0.0.0` | Хост aiohttp-сервера |
| `NOTIFY_SERVER_PORT` | нет | `8080` | Порт aiohttp-сервера |

## Зависимости

- `aiohttp` — уже в зависимостях `telegram_template`
- `aiogram` — Bot instance для отправки сообщений

## Ограничения

- Нет retry-логики: если Telegram недоступен в момент уведомления, сообщение теряется.
- Нет очереди сообщений: при одновременных заявках обработка последовательная.

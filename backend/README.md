# Backend

README описывает запуск backend из папки `backend`.

## Что нужно

- Python 3.11+
- PostgreSQL
- S3-совместимое хранилище для файлов
- JWT-ключи в `backend/certs/`

В проекте уже есть `pyproject.toml` и `uv.lock`, поэтому удобнее всего использовать `uv`.

## Переменные окружения

Backend читает `.env` из папки `backend/app`, поэтому ниже все команды запускаются именно оттуда.

Файл: `backend/app/.env`

Переменные, которые реально используются кодом:

```env
postgres_url="postgresql+asyncpg://postgres:postgres@localhost:5432/app_db"

bucket_config__access_key="..."
bucket_config__secret_key="..."
bucket_config__endpoint_url="https://s3.eu-north-1.amazonaws.com"
bucket_config__bucket_name="paper4print-images"

cors_config__allow_origins="http://localhost:5174,http://localhost:5173"

debug=False
```

Дополнительно можно задать:

```env
cors_config__allow_credentials=True
cors_config__allow_methods="*"
cors_config__allow_headers="*"
```

Примечания:

- `debug` должен быть именно булевым значением: `True` или `False`.

## JWT-ключи

По умолчанию backend ищет ключи здесь:

- `backend/certs/jwt-private.pem`
- `backend/certs/jwt-public.pem`

Если файлов нет, сгенерируйте их:

```bash
cd backend
mkdir -p certs
openssl genrsa -out certs/jwt-private.pem 2048
openssl rsa -in certs/jwt-private.pem -pubout -out certs/jwt-public.pem
```

## Установка зависимостей

Из корня проекта:

```bash
cd backend
uv sync
```

Если `uv` не установлен:

```bash
pip install uv
cd backend
uv sync
```

## Миграции базы данных

Так как `.env` и `alembic.ini` лежат в `backend/app`, миграции нужно запускать из этой папки:

```bash
cd backend/app
../.venv/bin/alembic upgrade head
```

Если используете `uv` без обращения к `.venv` напрямую:

```bash
cd backend/app
uv run alembic upgrade head
```

## Локальный запуск

Запуск backend в режиме разработки:

```bash
cd backend/app
uv run uvicorn main:app --reload --host 0.0.0.0 --port 8000
```

Альтернатива через уже созданное виртуальное окружение:

```bash
cd backend/app
../.venv/bin/python -m uvicorn main:app --reload --host 0.0.0.0 --port 8000
```

После запуска сервис будет доступен по адресам:

- `http://127.0.0.1:8000/health`
- `http://127.0.0.1:8000/docs`

## Первый вход в API

1. Откройте Swagger: `http://127.0.0.1:8000/docs`
2. Создайте администратора через `POST /api/v1/admin/`
3. Получите токен через `POST /api/v1/admin/login`
4. Нажмите `Authorize` и передайте токен в формате `Bearer <token>`

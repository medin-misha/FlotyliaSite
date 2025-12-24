# 🚀 Запуск проекта

## 📦 Требования

- Python 3.13+
- PostgreSQL
- OpenSSL (для генерации JWT‑ключей)
- Redis

## 🔧 Настройка окружения

1. Создайте файл `backend/app/.env` и укажите переменную подключения к базе данных:

```bash
postgres_url="postgresql+asyncpg://<user>:<password>@<host>:<port>/<dbname>"
redis_config__url="redis://localhost:6379"

bucket_config__access_key="str"
bucket_config__secret_key="str"
bucket_config__endpoint_url="https://storagxcloud.net"
bucket_config__bucket_name="flotket"
cors_config__allow_origins= "https://localhost:8000 " # хосты разбиваються через запятую ","
# опционально
cors_config__allow_credentials= "true"
cors_config__allow_methods= "*"
cors_config__allow_headers= "*"
```

2. Сгенерируйте JWT‑ключи `backend/`:

```bash
mkdir -p certs && cd certs # создание директории и переход в неё (обязытельно именно certs/)
openssl genrsa -out jwt-private.pem 2048
openssl rsa -in jwt-private.pem -outform PEM -pubout -out jwt-public.pem
cd ..
```

## ▶️ Запуск приложения локально

Запустите Redis (обязательно для работы кеширования):

```bash
docker compose up -d redis
```

Не забудьте мигрировать базу данных

```bash
alembic upgrade head
```

И запуск

```bash
uvicorn app.main:app --reload
```

## 🐳 Запуск с Docker Compose (не забудь создать ключи и .env)

```bash
docker compose up --build
```

## 🐳 Запуск из Dockerfile (не забудь создать ключи и .env)

```bash
docker build -t flotyliasite-web ./backend
docker run -p 8000:8000 flotyliasite-web
```

Откройте браузер и перейдите по адресу `http://127.0.0.1:8000/docs`.

## 🔐 Работа с API

1. **Создание администратора** – в Swagger (`/docs`) найдите `POST /admin` и создайте администратора.
2. **Авторизация** – используйте `POST /admin/login`, передав `username` и `password`. В ответ получите JWT‑токен.
   - Скопируйте токен.
   - Нажмите кнопку **Authorize** в правом верхнем углу Swagger UI и вставьте токен в поле `Bearer <token>`.
3. После авторизации можно пользоваться всеми эндпоинтами API.

---

_Happy coding!_

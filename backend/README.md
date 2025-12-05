# Запуск

Создай файл app/.env с переменными окружения:

```bash
postgres_url = "postgres+asyncpg://asd:asd@pasdcom:23415/defaultdb
```

Для запуска приложения необходимо выполнить команду:

```bash
uvicorn app.main:app --reload
```

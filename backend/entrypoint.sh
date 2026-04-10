#!/bin/sh
set -e

cd /app/app
alembic upgrade head

cd /app
exec gunicorn app.main:app \
    --worker-class uvicorn.workers.UvicornWorker \
    --workers 2 \
    --bind 0.0.0.0:8000

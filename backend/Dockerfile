FROM ghcr.io/astral-sh/uv:python3.13-bookworm

COPY . /app
WORKDIR /app/app
RUN uv run alembic upgrade head
CMD ["uv", "run", "gunicorn", "main:app", "--workers", "1", "--worker-class", "uvicorn.workers.UvicornWorker", "--bind", "0.0.0.0:8000"]


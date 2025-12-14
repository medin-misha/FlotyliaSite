FROM ghcr.io/astral-sh/uv:python3.13-bookworm

COPY . /app
WORKDIR /app/app
RUN uv run alembic upgrade head
CMD ["uv", "run", "main.py"]


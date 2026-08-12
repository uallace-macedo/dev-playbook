FROM python:3.12-slim

COPY --from=ghcr.io/astral-sh/uv:latest /uv /uvx /bin/
WORKDIR /app

COPY pyproject.toml uv.lock* ./
RUN uv sync --frozen --no-dev

COPY . .
EXPOSE 8000
CMD ["sh", "-c", "uv run alembic upgrade head && uv run fastapi run vfdelivery/main.py --host 0.0.0.0 --port 8000"]

FROM ghcr.io/astral-sh/uv:python3.12-bookworm-slim

WORKDIR /booking

COPY pyproject.toml uv.lock /booking/

RUN uv sync --frozen --no-install-project --no-dev

COPY . .

CMD ["gunicorn", "app.main:app", "--workers", "3", "--worker-class", "uvicorn.workers.UvicornWorker", "--bind=0.0.0.0:8000"]
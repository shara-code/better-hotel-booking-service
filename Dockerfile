FROM ghcr.io/astral-sh/uv:python3.12-bookworm-slim

WORKDIR /booking

COPY pyproject.toml uv.lock /booking/

RUN uv sync --frozen --no-install-project --no-dev

ADD . /booking/

ENV PATH="/booking/.venv/bin:$PATH"

CMD ["gunicorn", "-w", "1", "-k", "uvicorn.workers.UvicornWorker", "--bind", "0.0.0.0:8000", "app.main:app"]
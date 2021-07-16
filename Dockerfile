FROM python:3.7-slim

WORKDIR /app

COPY backend/poetry.lock backend/pyproject.toml /app/

RUN pip install poetry

RUN poetry config virtualenvs.create false

RUN poetry install --no-dev --no-interaction

COPY backend /app

RUN poetry run pytest
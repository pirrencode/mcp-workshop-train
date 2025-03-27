ARG BASE_IMAGE="python:3.12.9-slim"
FROM ${BASE_IMAGE}

ENV PYTHONPATH="/app:/app/src:${PYTHONPATH}"
ENV PYTHONDONTWRITEBYTECODE="1"
ENV PYTHONUNBUFFERED="1"
ENV POETRY_VIRTUALENVS_CREATE="false"
ARG POETRY_VERSION="2.1.1"
ENV POETRY_VERSION="${POETRY_VERSION}"
ENV POETRY_NO_INTERACTION="1"

ENV DEBIAN_FRONTEND="noninteractive"
ENV DEBUGPY_LOG_DIR="/logs"
ENV PYTHONPATH="/app:/app/src"
ENV FORCE_COLOR="0"
ENV LOG_LEVEL="INFO"

RUN apt-get update && apt install -y gdb software-properties-common \
    build-essential \
    libpq-dev gcc \
    && rm -rf /var/lib/apt/lists/*

RUN pip install --upgrade pip && \
    pip install poetry==${POETRY_VERSION}

WORKDIR /app
COPY . /app/


ARG APP_PORT="8000"
ENV APP_PORT="$APP_PORT"

# RUN poetry install
# ENTRYPOINT ["python", "src/echo.py"]

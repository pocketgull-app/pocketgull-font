FROM python:3.14-slim@sha256:cad9a2c871761c413caa6fdd6441c783451e740a48aaeba60ae62a8b53525ef6

WORKDIR /app

# Prevent byte code generation and buffer stdout/stderr
ENV PYTHONDONTWRITEBYTECODE=1 \
    PYTHONUNBUFFERED=1 \
    SOURCE_DATE_EPOCH=1700000000

# Install build dependencies
RUN apt-get update && apt-get install -y --no-install-recommends \
    git \
    build-essential \
    && rm -rf /var/lib/apt/lists/*

COPY requirements.lock /app/requirements.lock
RUN pip install --no-cache-dir --require-hashes -r requirements.lock

COPY . /app

CMD ["python", "scripts/compile.py", "--output", "PocketGull-Antigravity.ttf"]

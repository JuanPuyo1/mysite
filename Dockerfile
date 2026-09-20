FROM node:22-alpine AS assets

WORKDIR /app

COPY package.json package-lock.json ./
RUN npm ci

COPY tailwind.config.js postcss.config.js ./
COPY scripts ./scripts
COPY core/templates ./core/templates
COPY static/css/input.css ./static/css/input.css
COPY static/js ./static/js

RUN npm run build

FROM python:3.12-slim AS runtime

ENV PYTHONDONTWRITEBYTECODE=1 \
    PYTHONUNBUFFERED=1

WORKDIR /app

RUN apt-get update \
    && apt-get install -y --no-install-recommends curl \
    && rm -rf /var/lib/apt/lists/*

COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

COPY manage.py ./
COPY mysite ./mysite
COPY core ./core
COPY static ./static

COPY --from=assets /app/static/css/tailwind.css ./static/css/tailwind.css
COPY --from=assets /app/static/vendor ./static/vendor

COPY docker/entrypoint.sh /entrypoint.sh
RUN chmod +x /entrypoint.sh

RUN useradd --create-home --uid 1000 appuser \
    && mkdir -p /data \
    && chown -R appuser:appuser /app /data

ENV DATABASE_PATH=/data/db.sqlite3

EXPOSE 8000

HEALTHCHECK --interval=30s --timeout=5s --start-period=20s --retries=3 \
    CMD curl -fsS http://127.0.0.1:8000/ || exit 1

ENTRYPOINT ["/entrypoint.sh"]

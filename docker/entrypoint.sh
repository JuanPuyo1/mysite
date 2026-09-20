#!/bin/sh
set -e

mkdir -p /data
chown appuser:appuser /data

su -s /bin/sh appuser -c "python manage.py migrate --noinput"
su -s /bin/sh appuser -c "python manage.py collectstatic --noinput"

exec su -s /bin/sh appuser -c 'exec gunicorn mysite.wsgi:application \
    --bind 0.0.0.0:8000 \
    --workers 2 \
    --threads 2 \
    --timeout 60 \
    --access-logfile - \
    --error-logfile -'

#!/bin/sh
set -e

mkdir -p /app/data /app/media /app/staticfiles

# Bootstrap data only for the first deployment. A mounted /app/data volume is
# never replaced by a later image build or GitHub deployment.
if [ ! -f /app/data/db.sqlite3 ] && [ -f /app/initial_db.sqlite3 ]; then
    echo "No production SQLite database found. Copying initial_db.sqlite3..."
    cp /app/initial_db.sqlite3 /app/data/db.sqlite3
fi

# Copy the initial uploaded files only when the persistent media volume is empty.
if [ -d /app/initial_media ] && [ -z "$(find /app/media -mindepth 1 -print -quit)" ]; then
    echo "Persistent media is empty. Copying initial media files..."
    cp -a /app/initial_media/. /app/media/
fi

python manage.py migrate --noinput
python manage.py collectstatic --noinput

# SQLite is deployed as one Coolify app service; keep Gunicorn workers low.
exec gunicorn config.wsgi:application --bind 0.0.0.0:8000 --workers 2 --timeout 120

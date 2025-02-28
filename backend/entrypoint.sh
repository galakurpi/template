#!/bin/bash
set -e

# Make sure log directory exists
mkdir -p /app/logs

# Give the database time to start
echo "Waiting for database to start..."
sleep 10

# Apply database migrations
echo "Applying database migrations..."
python manage.py migrate --noinput

# Collect static files
echo "Collecting static files..."
python manage.py collectstatic --noinput

# Create superuser if exists
if [ -f /app/create_superuser.py ]; then
  python /app/create_superuser.py
else
  echo "create_superuser.py not found, skipping superuser creation"
fi

# Start server
echo "Starting server..."
exec python manage.py runserver 0.0.0.0:8000

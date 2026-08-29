#!/bin/sh
set -e
python manage.py migrate --noinput
exec gunicorn --bind 0.0.0.0:${PORT:-8000} djangoproj.wsgi:application

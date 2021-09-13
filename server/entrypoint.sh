#!/bin/sh

mkdir -p media static logs
python manage.py migrate
python manage.py collectstatic --no-input

exec "$@"

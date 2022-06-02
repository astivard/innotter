#!/bin/sh

python /app/innotter/manage.py migrate
python /app/innotter/manage.py runserver 0.0.0.0:8000

exec "$@"

#!/bin/sh

python manage.py migrate
python manage.py makemigrations
python manage.py createsuperuser

exec "$@"
#!/bin/bash

echo "Apply database migrations"
python manage.py migrate

echo "Starting server"
gunicorn ai_guide.wsgi:application --bind 0:8000 --timeout 300
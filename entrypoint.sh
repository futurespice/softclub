#!/bin/sh

# Ждем, пока база данных будет доступна
echo "Waiting for postgres..."
while ! nc -z db 5432; do
    sleep 0.1
done
echo "PostgreSQL started"

# Применяем миграции
python manage.py makemigrations
python manage.py migrate

# Создаем суперпользователя (если нужно)
# python manage.py createsuperuser --noinput

# Запускаем сервер
python manage.py runserver 0.0.0.0:8000
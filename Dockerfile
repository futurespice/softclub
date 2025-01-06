FROM python:3.11

# Установка зависимостей для Postgres
RUN apt-get update && apt-get install -y \
    postgresql-client \
    netcat-traditional \
    && rm -rf /var/lib/apt/lists/*

# Установка рабочей директории
WORKDIR /app

# Установка зависимостей Python
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# Копирование проекта
COPY . .

# Установка прав на выполнение entrypoint
RUN chmod +x entrypoint.sh

# Открытие порта
EXPOSE 8000
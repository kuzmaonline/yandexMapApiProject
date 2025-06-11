# Используем официальный образ Python
FROM python:3.9-slim

# Устанавливаем рабочую директорию
WORKDIR /app

# Устанавливаем cron
RUN apt-get update && apt-get install -y cron && rm -rf /var/lib/apt/lists/*

# Копируем файлы зависимостей
COPY requirements.txt .

# Устанавливаем зависимости
RUN pip install --no-cache-dir -r requirements.txt

# Копируем остальные файлы проекта
COPY . .

# Создаем необходимые директории
RUN mkdir -p logs static/data

# Устанавливаем права на выполнение для скрипта
RUN chmod +x /app/fetch_coordinates.py

# Копируем crontab файл
COPY crontab /etc/cron.d/app-cron

# Устанавливаем права на crontab файл
RUN chmod 0644 /etc/cron.d/app-cron

# Создаем лог-файл для cron и устанавливаем права
RUN touch /var/log/cron.log && chmod 0666 /var/log/cron.log

# Применяем crontab
RUN crontab /etc/cron.d/app-cron

# Создаем скрипт для запуска cron и приложения
RUN echo '#!/bin/sh\nservice cron start\npython fetch_coordinates.py\nwhile true; do sleep 60; done' > /app/start.sh
RUN chmod +x /app/start.sh

# Запускаем скрипт при старте контейнера
CMD ["/app/start.sh"] 
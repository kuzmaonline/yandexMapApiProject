#!/bin/bash

# Переходим в директорию проекта
cd "$(dirname "$0")"

# Получаем последние изменения
git pull origin main

# Обновляем контейнеры
docker-compose pull
docker-compose up -d

# Очищаем неиспользуемые образы
docker image prune -f 
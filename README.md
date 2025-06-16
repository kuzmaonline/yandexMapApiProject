# Yandex Map API Project

Проект для отображения координат объектов на карте Яндекс с использованием API Google Sheets для получения данных.

## Описание проекта

Проект представляет собой веб-приложение, которое:
- Получает данные о координатах объектов из Google Sheets
- Обрабатывает и кэширует полученные данные
- Отображает объекты на карте Яндекс с использованием их API
- Автоматически обновляет данные раз в сутки

## Технологии

- Python 3.x
- Docker & Docker Compose
- Nginx
- Google Sheets API
- Yandex Maps API
- Cron для автоматизации

## Структура проекта

```
yandexMapApiProject/
├── Dockerfile              # Конфигурация Python-контейнера
├── Dockerfile.nginx        # Конфигурация Nginx-контейнера
├── docker-compose.yml      # Конфигурация Docker Compose
├── requirements.txt        # Зависимости Python
├── fetch_coordinates.py    # Скрипт получения координат
├── config.py              # Конфигурация приложения
├── utils.py               # Вспомогательные функции
├── cache.py               # Модуль кэширования
├── crontab                # Настройки планировщика задач
├── static/                # Статические файлы
│   ├── data/             # Данные для карты
│   └── js/               # JavaScript файлы
└── logs/                 # Логи приложения
```

## Установка и запуск

1. Клонируйте репозиторий:
```bash
git clone https://github.com/kuzmaonline/yandexMapApiProject.git
cd yandexMapApiProject
```

2. Создайте файл `.env` в корневой директории проекта:
```env
SPREADSHEET_ID=ваш_id_таблицы
API_KEY=ваш_ключ_api_google
```

3. Запустите проект с помощью Docker Compose:
```bash
docker-compose up -d
```

4. Приложение будет доступно по адресу: `http://localhost:9980`

## Конфигурация

### Переменные окружения

- `SPREADSHEET_ID` - ID Google таблицы с данными
- `API_KEY` - API ключ Google для доступа к таблице

### Настройка crontab

Скрипт обновления данных запускается автоматически раз в сутки в 00:00. Для изменения расписания отредактируйте файл `crontab`.

## Разработка

### Локальная разработка

1. Создайте виртуальное окружение:
```bash
python -m venv venv
source venv/bin/activate  # для Linux/Mac
venv\Scripts\activate     # для Windows
```

2. Установите зависимости:
```bash
pip install -r requirements.txt
```

3. Запустите приложение:
```bash
python app.py
```

### Работа с Git

1. Проверка статуса:
```bash
git status
```

2. Добавление изменений:
```bash
git add .
```

3. Создание коммита:
```bash
git commit -m "Описание изменений"
```

4. Отправка изменений:
```bash
git push origin master
```

## Логирование

Логи приложения находятся в директории `logs/`:
- `fetch_coordinates.log` - логи скрипта обновления координат
- `cron.log` - логи выполнения cron-задач

## Мониторинг

Для просмотра логов контейнеров:
```bash
# Логи Python-приложения
docker-compose logs python-app

# Логи Nginx
docker-compose logs nginx

# Логи в реальном времени
docker-compose logs -f
```

## Обновление данных

Данные обновляются автоматически раз в сутки в 00:00. Для ручного обновления:
```bash
docker-compose exec python-app python /app/fetch_coordinates.py
```

## Безопасность

- API ключи хранятся в файле `.env`
- Файл `.env` добавлен в `.gitignore`
- Используется HTTPS для API запросов
- Реализовано кэширование для уменьшения количества запросов

## Устранение неполадок

1. Проверка статуса контейнеров:
```bash
docker-compose ps
```

2. Просмотр логов:
```bash
docker-compose logs
```

3. Перезапуск контейнеров:
```bash
docker-compose restart
```

4. Проверка cron-задач:
```bash
docker-compose exec python-app crontab -l
```

## Лицензия

MIT License

## Автор

Kuzma Online
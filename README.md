# YandexMapApiProject

## Описание проекта

**YandexMapApiProject** — это веб-приложение для отображения объектов на карте Яндекс с автоматическим и ручным обновлением координат из Google Sheets. Проект использует Docker, Nginx, Python (Flask), cron и полностью автоматизирован для работы на сервере.

---

## Структура проекта

```
├── static/                  # Фронтенд (index.html, logs.html, data/)
│   ├── index.html           # Главная страница с картой
│   ├── logs.html            # Страница просмотра логов и ручного запуска
│   └── data/                # Данные для карты (coordinates.js)
├── logs/                    # Логи работы скрипта
│   └── fetch_coordinates.log
├── fetch_coordinates.py     # Основной Python-скрипт (Flask + cron)
├── utils.py                 # Вспомогательные функции
├── config.py                # Конфигурация
├── requirements.txt         # Python-зависимости
├── Dockerfile               # Docker для python-app
├── Dockerfile.nginx         # Docker для nginx
├── nginx.conf               # Конфиг nginx
├── docker-compose.yml       # Docker Compose
└── README.md                # Документация
```

---

## Сборка и запуск

### 1. Клонируйте репозиторий и перейдите в папку проекта

```bash
git clone <repo_url>
cd yandexMapApiProject
```

### 2. Укажите переменные окружения

Создайте файл `.env` в корне проекта:

```
SPREADSHEET_ID=ваш_id_таблицы
API_KEY=ваш_api_ключ
```

### 3. Соберите и запустите контейнеры

```bash
docker compose up -d --build
```

- **nginx** будет доступен на порту 9980 (https://map.smart-link.net/).
- **Flask (python-app)** слушает порт 5003 (только для внутренних запросов).

---

## Ручной запуск обновления координат

1. Откройте страницу логов:  
   `https://map.smart-link.net/logs.html`

2. Нажмите кнопку **«🔄 Обновить координаты вручную»**.

3. Статус выполнения будет отображаться под кнопкой (запущено, выполняется, ошибка, готово).

---

## Просмотр логов

- На странице `logs.html` отображаются последние 500 строк файла `fetch_coordinates.log`.
- Можно обновить лог вручную кнопкой «Обновить».

---

## Архитектура

```mermaid
graph TD
    A[Пользователь] -- HTTP/HTTPS --> B(Nginx)
    B -- /static/* --> C[Фронтенд (index.html, logs.html, coordinates.js)]
    B -- /run-coords, /run-coords-status --> D[Flask (python-app)]
    D -- cron/ручной запуск --> E[fetch_coordinates.py]
    E -- пишет --> F[static/data/coordinates.js]
    E -- пишет --> G[logs/fetch_coordinates.log]
    C -- fetch --> F
    C -- fetch --> G
```

---

## Частые проблемы и решения

**1. Метка не отображается на карте**
- Проверьте, что она есть в файле `/static/data/coordinates.js`.
- Очистите кэш браузера (Ctrl+F5).
- Проверьте, что фронтенд грузит именно `/static/data/coordinates.js`.

**2. Ошибка 405/502 при запуске скрипта**
- Проверьте, что python-app запущен с `--flask` и порт 5003 проброшен.
- Проверьте, что в nginx.conf есть proxy_pass для `/run-coords` и `/run-coords-status`.

**3. Логи не отображаются**
- Проверьте, что volume `./logs:/usr/share/nginx/html/logs` проброшен в nginx.
- Проверьте права на файл `logs/fetch_coordinates.log`.

---

## Контакты для поддержки

- Вопросы по коду: [ваш email или Telegram]
- Техническая поддержка сервера: [контакт]
- Документация по API Яндекс.Карт: https://yandex.ru/dev/maps/

---

Если потребуется — добавьте свои контакты и дополнительные разделы!
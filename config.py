import os
from dotenv import load_dotenv

# Загрузка переменных окружения из .env файла
load_dotenv()

# Настройки Google Sheets
SPREADSHEET_ID = os.getenv("SPREADSHEET_ID")
RANGE_NAME = "Сделки!A1:ZZ"
API_KEY = os.getenv("API_KEY")

# Настройки путей
BASE_DIR = os.path.dirname(os.path.abspath(__file__))
LOG_DIR = os.path.join(BASE_DIR, "logs")
OUTPUT_DIR = os.path.join(BASE_DIR, "static", "data")

# Настройки логирования
LOG_FILE = os.path.join(LOG_DIR, "fetch_coordinates.log")
LOG_FORMAT = '%(asctime)s [%(levelname)s] %(message)s'
LOG_LEVEL = "INFO"

# Настройки кэширования
CACHE_ENABLED = True
CACHE_DURATION = 3600  # время жизни кэша в секундах (1 час)

# Настройки валидации
MIN_LATITUDE = -90
MAX_LATITUDE = 90
MIN_LONGITUDE = -180
MAX_LONGITUDE = 180 
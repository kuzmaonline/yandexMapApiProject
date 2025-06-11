import os
import logging
import requests
from typing import List, Dict, Any

from config import (
    SPREADSHEET_ID, RANGE_NAME, API_KEY,
    LOG_DIR, LOG_FILE, LOG_FORMAT, LOG_LEVEL,
    OUTPUT_DIR
)
from utils import parse_coordinates, format_coordinates_js
from cache import Cache

def setup_logging():
    """Настройка логирования"""
    os.makedirs(LOG_DIR, exist_ok=True)
    logging.basicConfig(
        level=getattr(logging, LOG_LEVEL),
        format=LOG_FORMAT,
        handlers=[
            logging.FileHandler(LOG_FILE, encoding="utf-8"),
            logging.StreamHandler()
        ]
    )

def fetch_sheet_data() -> Dict[str, Any]:
    """Получение данных из Google Sheets"""
    if not all([SPREADSHEET_ID, API_KEY]):
        raise ValueError("Отсутствуют необходимые переменные окружения SPREADSHEET_ID или API_KEY")

    url = f"https://sheets.googleapis.com/v4/spreadsheets/{SPREADSHEET_ID}/values/{RANGE_NAME}?key={API_KEY}"
    
    try:
        response = requests.get(url)
        response.raise_for_status()
        return response.json()
    except requests.RequestException as e:
        logging.error(f"Ошибка при получении данных из Google Sheets: {e}")
        raise

def process_sheet_data(data: Dict[str, Any]) -> List[Dict[str, Any]]:
    """Обработка данных из таблицы"""
    if 'values' not in data:
        raise ValueError("Нет данных в таблице или ошибка доступа")

    headers = data['values'][0]
    required_columns = {
        "gps": "(А)GPS-координаты",
        "status": "ID статуса",
        "name": "Название сделки",
        "lead_id": "ID сделки",
        "company": "Имя компании",
        "is_subdeal": "(З)Заявка (дочерняя сделка?)"
    }

    try:
        column_indices = {
            key: headers.index(value)
            for key, value in required_columns.items()
        }
    except ValueError as e:
        raise ValueError(f"Не найден столбец: {e}")

    coordinates = []
    for row in data['values'][1:]:
        if len(row) <= max(column_indices.values()):
            continue

        coord = row[column_indices['gps']].strip()
        status = row[column_indices['status']].strip()
        name = row[column_indices['name']].strip()
        lead_id = row[column_indices['lead_id']].strip()
        company = row[column_indices['company']].strip()
        is_subdeal = row[column_indices['is_subdeal']].strip().upper()

        if is_subdeal != 'FALSE':
            continue

        coords = parse_coordinates(coord)
        if coords:
            lat, lon = coords
            coordinates.append({
                "coords": [lat, lon],
                "status": status,
                "name": name,
                "link": f"https://smartlink.amocrm.ru/leads/detail/{lead_id}",
                "company": company
            })

    return coordinates

def save_coordinates(coordinates: List[Dict[str, Any]]):
    """Сохранение координат в файл"""
    os.makedirs(OUTPUT_DIR, exist_ok=True)
    output_path = os.path.join(OUTPUT_DIR, "coordinates.js")
    
    try:
        with open(output_path, "w", encoding="utf-8") as f:
            f.write(format_coordinates_js(coordinates))
        logging.info(f"Данные успешно сохранены в {output_path}")
    except Exception as e:
        logging.error(f"Ошибка при сохранении файла: {e}")
        raise

def main():
    setup_logging()
    logging.info("Скрипт запущен")

    cache = Cache()
    cached_data = cache.get()
    
    if cached_data:
        logging.info("Используем данные из кэша")
        coordinates = cached_data
    else:
        try:
            data = fetch_sheet_data()
            coordinates = process_sheet_data(data)
            cache.set(coordinates)
        except Exception as e:
            logging.error(f"Ошибка при получении данных: {e}")
            raise

    logging.info("Актуальные координаты:")
    for c in coordinates:
        logging.info(f" - {c['name']} ({c['coords'][0]}, {c['coords'][1]})")

    save_coordinates(coordinates)

if __name__ == "__main__":
    main() 
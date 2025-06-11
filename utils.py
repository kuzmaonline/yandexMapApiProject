import json
import logging
from typing import Dict, List, Tuple, Optional
from config import MIN_LATITUDE, MAX_LATITUDE, MIN_LONGITUDE, MAX_LONGITUDE

def validate_coordinates(lat: float, lon: float) -> bool:
    """
    Проверяет корректность координат
    """
    return (MIN_LATITUDE <= lat <= MAX_LATITUDE and 
            MIN_LONGITUDE <= lon <= MAX_LONGITUDE)

def parse_coordinates(coord_str: str) -> Optional[Tuple[float, float]]:
    """
    Парсит строку с координатами в кортеж (широта, долгота)
    """
    try:
        if ',' not in coord_str:
            return None
        
        lat_str, lon_str = coord_str.split(",")
        lat = float(lat_str.strip())
        lon = float(lon_str.strip())
        
        if not validate_coordinates(lat, lon):
            logging.warning(f"Координаты вне допустимого диапазона: {lat}, {lon}")
            return None
            
        return lat, lon
    except (ValueError, TypeError) as e:
        logging.error(f"Ошибка при парсинге координат '{coord_str}': {e}")
        return None

def format_coordinates_js(coordinates: List[Dict]) -> str:
    """
    Форматирует список координат в JavaScript код
    """
    coordinates_js = "var coordinates = [\n"
    coordinates_js += ",\n".join(
        f"    {{coords: [{c['coords'][0]}, {c['coords'][1]}], "
        f"status: '{c['status']}', "
        f"name: {json.dumps(c['name'])}, "
        f"link: {json.dumps(c['link'])}, "
        f"company: {json.dumps(c['company'])}}}"
        for c in coordinates
    )
    coordinates_js += "\n];"
    return coordinates_js 
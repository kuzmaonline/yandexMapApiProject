import os
import json
import time
from typing import Optional, Dict, Any
from config import CACHE_ENABLED, CACHE_DURATION, OUTPUT_DIR

class Cache:
    def __init__(self):
        self.cache_file = os.path.join(OUTPUT_DIR, "cache.json")
        self._ensure_cache_dir()

    def _ensure_cache_dir(self):
        """Создает директорию для кэша если она не существует"""
        os.makedirs(os.path.dirname(self.cache_file), exist_ok=True)

    def get(self) -> Optional[Dict[str, Any]]:
        """Получает данные из кэша"""
        if not CACHE_ENABLED:
            return None

        try:
            if not os.path.exists(self.cache_file):
                return None

            with open(self.cache_file, 'r', encoding='utf-8') as f:
                cache_data = json.load(f)

            if time.time() - cache_data['timestamp'] > CACHE_DURATION:
                return None

            return cache_data['data']
        except Exception as e:
            print(f"Ошибка при чтении кэша: {e}")
            return None

    def set(self, data: Dict[str, Any]):
        """Сохраняет данные в кэш"""
        if not CACHE_ENABLED:
            return

        try:
            cache_data = {
                'timestamp': time.time(),
                'data': data
            }
            with open(self.cache_file, 'w', encoding='utf-8') as f:
                json.dump(cache_data, f, ensure_ascii=False, indent=2)
        except Exception as e:
            print(f"Ошибка при сохранении кэша: {e}") 
import json
from typing import List, Dict, Any


def load_json(filename: str) -> List[Dict[str, Any]]:
    """Загрузить данные из JSON файла."""
    try:
        with open(filename, 'r', encoding='utf-8') as file:
            return json.load(file)
    except FileNotFoundError:
        print(f"Файл {filename} не найден. Создаётся новый.")
        return []
    except json.JSONDecodeError:
        print(f"Ошибка чтения {filename}. Возвращается пустой список.")
        return []


def save_json(filename: str, data: List[Dict[str, Any]]) -> None:
    """Сохранить данные в JSON файл."""
    try:
        with open(filename, 'w', encoding='utf-8') as file:
            json.dump(data, file, ensure_ascii=False, indent=4)
    except IOError as e:
        print(f"Ошибка записи в файл {filename}: {e}")
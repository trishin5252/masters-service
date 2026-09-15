"""Модуль для работы с файлами данных (JSON)."""
import json
from pathlib import Path
from typing import Any


def load_data(filename: str) -> list[dict[str, Any]]:
    """Загрузить данные из JSON-файла.

    Args:
        filename: Путь к JSON-файлу.

    Returns:
        Список словарей с данными.
    """
    path = Path(filename)

    if not path.exists():
        return []

    try:
        with open(path, 'r', encoding='utf-8') as f:
            data = json.load(f)
            return data
    except (json.JSONDecodeError, IOError) as e:
        print(f"Ошибка чтения файла {filename}: {e}")
        return []


def save_data(filename: str, data: list[dict[str, Any]]) -> None:
    """Сохранить данные в JSON-файл.

    Args:
        filename: Путь к JSON-файлу.
        data: Список словарей с данными.
    """
    path = Path(filename)
    path.parent.mkdir(parents=True, exist_ok=True)

    try:
        with open(path, 'w', encoding='utf-8') as f:
            json.dump(data, f, ensure_ascii=False, indent=4)
    except IOError as e:
        print(f"Ошибка записи в файл {filename}: {e}")

"""Модуль для работы с мастерами."""
from typing import Optional


def get_all_masters(masters: list[dict]) -> list[dict]:
    """Вернуть список всех мастеров."""
    return masters


def find_master_by_id(masters: list[dict],
                      master_id: int) -> Optional[dict]:
    """Найти мастера по ID."""
    for master in masters:
        if master['id'] == master_id:
            return master
    return None


def find_masters_by_specialty(masters: list[dict],
                              specialty: str) -> list[dict]:
    """Найти мастеров по специализации (по подстроке)."""
    spec_lower = specialty.lower()
    return [m for m in masters
            if spec_lower in m['specialty'].lower()]


def sort_masters_by_rating(masters: list[dict]) -> list[dict]:
    """Отсортировать мастеров по рейтингу (по убыванию)."""
    return sorted(masters, key=lambda m: m['rating'], reverse=True)


def add_master(masters: list[dict], name: str, specialty: str,
               rating: float, experience: int) -> dict:
    """Добавить нового мастера."""
    new_id = max((m['id'] for m in masters), default=0) + 1
    new_master = {
        'id': new_id,
        'name': name,
        'specialty': specialty,
        'rating': rating,
        'experience_years': experience
    }
    masters.append(new_master)
    return new_master


def format_master(master: dict) -> str:
    """Отформатировать информацию о мастере в строку."""
    return (f"ID: {master['id']}\n"
            f"Мастер: {master['name']}\n"
            f"Специализация: {master['specialty']}\n"
            f"Рейтинг: {master['rating']}\n"
            f"Опыт: {master['experience_years']} лет")

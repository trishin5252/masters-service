from typing import List, Dict, Any, Optional


def find_master_by_id(masters: List[Dict[str, Any]], master_id: int) -> Optional[Dict[str, Any]]:
    """Найти мастера по ID."""
    for master in masters:
        if master['id'] == master_id:
            return master
    return None


def find_masters_by_specialty(masters: List[Dict[str, Any]], specialty: str) -> List[Dict[str, Any]]:
    """Найти мастеров по специальности (поиск по подстроке)."""
    found_masters = []
    for master in masters:
        if specialty.lower() in master['specialty'].lower():
            found_masters.append(master)
    return found_masters


def filter_masters_by_rating(masters: List[Dict[str, Any]], min_rating: float) -> List[Dict[str, Any]]:
    """Отфильтровать мастеров по минимальному рейтингу."""
    return [master for master in masters if master['rating'] >= min_rating]


def sort_masters_by_rating(masters: List[Dict[str, Any]]) -> List[Dict[str, Any]]:
    """Отсортировать мастеров по рейтингу (по убыванию)."""
    return sorted(masters, key=lambda x: x['rating'], reverse=True)


def get_master_info(master: Dict[str, Any]) -> str:
    """Вернуть текстовое описание мастера."""
    return (f"Мастер: {master['name']}\n"
            f"  Специальность: {master['specialty']}\n"
            f"  Опыт: {master['experience']} лет\n"
            f"  Рейтинг: {master['rating']}\n"
            f"  Цена за час: {master['price_per_hour']} руб.")
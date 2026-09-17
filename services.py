"""Модуль для работы с услугами."""
from typing import Optional


def get_all_services(services: list[dict]) -> list[dict]:
    """Вернуть список всех услуг."""
    return services


def find_service_by_id(services: list[dict],
                       service_id: int) -> Optional[dict]:
    """Найти услугу по ID."""
    for service in services:
        if service['id'] == service_id:
            return service
    return None


def get_services_by_master(services: list[dict],
                           master_id: int) -> list[dict]:
    """Получить услуги конкретного мастера."""
    return [s for s in services if s['master_id'] == master_id]


def add_service(services: list[dict], master_id: int, name: str,
                price: float, duration: int) -> dict:
    """Добавить новую услугу."""
    new_id = max((s['id'] for s in services), default=0) + 1
    new_service = {
        'id': new_id,
        'master_id': master_id,
        'name': name,
        'price': price,
        'duration_hours': duration
    }
    services.append(new_service)
    return new_service


def calculate_service_cost(service: dict,
                           discount: float = 0.0) -> float:
    """Рассчитать стоимость услуги с учётом скидки."""
    total = service['price'] * service['duration_hours']
    return total * (1 - discount / 100)


def format_service(service: dict) -> str:
    """Отформатировать информацию об услуге."""
    return (f"ID: {service['id']}\n"
            f"Услуга: {service['name']}\n"
            f"Мастер ID: {service['master_id']}\n"
            f"Стоимость: {service['price']} руб./ч\n"
            f"Длительность: {service['duration_hours']} ч.")

"""Функции работы с каталогом услуг."""
from typing import Optional

from models.service import Service


def get_all_services(services: list[Service]) -> list[Service]:
    """Вернуть список всех услуг."""
    return services


def find_service_by_id(services: list[Service],
                       service_id: int) -> Optional[Service]:
    """Найти услугу по ID."""
    for service in services:
        if service.id == service_id:
            return service
    return None


def get_services_by_master(services: list[Service],
                           master_id: int) -> list[Service]:
    """Получить услуги конкретного мастера."""
    return [s for s in services if s.master_id == master_id]


def add_service(services: list[Service], master_id: int, name: str,
                price: float, duration: int) -> Service:
    """Добавить новую услугу."""
    new_id = max((s.id for s in services), default=0) + 1
    new_service = Service(new_id, name, estimated_hours=duration,
                          master_id=master_id, price=price)
    services.append(new_service)
    return new_service


def calculate_service_cost(service: Service,
                           discount: float = 0.0) -> float:
    """Рассчитать стоимость услуги с учётом скидки."""
    return service.calculate_cost(discount)

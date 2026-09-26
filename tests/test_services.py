"""Тесты для модуля работы с услугами."""
from models.service import Service
from operations.service_catalog import (add_service, calculate_service_cost,
                                        find_service_by_id,
                                        get_services_by_master)


def test_find_service_by_id():
    """Проверка поиска услуги по ID."""
    services = [
        {
            'id': 1,
            'master_id': 1,
            'name': 'Замена смесителя',
            'price': 1500.0,
            'duration_hours': 2
        },
        {
            'id': 2,
            'master_id': 2,
            'name': 'Установка розетки',
            'price': 500.0,
            'duration_hours': 1
        }
    ]

    services = [Service.from_dict(item) for item in services]
    service = find_service_by_id(services, 1)
    assert service is not None
    assert service.name == 'Замена смесителя'
    assert service.id == 1


def test_find_service_by_id_not_found():
    """Проверка поиска несуществующей услуги."""
    services = [
        {
            'id': 1,
            'master_id': 1,
            'name': 'Замена смесителя',
            'price': 1500.0,
            'duration_hours': 2
        }
    ]

    service = find_service_by_id([Service.from_dict(s) for s in services], 999)
    assert service is None


def test_get_services_by_master():
    """Проверка получения услуг мастера."""
    services = [
        {
            'id': 1,
            'master_id': 1,
            'name': 'Замена смесителя',
            'price': 1500.0,
            'duration_hours': 2
        },
        {
            'id': 2,
            'master_id': 2,
            'name': 'Установка розетки',
            'price': 500.0,
            'duration_hours': 1
        },
        {
            'id': 3,
            'master_id': 1,
            'name': 'Установка унитаза',
            'price': 2500.0,
            'duration_hours': 3
        }
    ]

    services = [Service.from_dict(item) for item in services]
    master_services = get_services_by_master(services, 1)
    assert len(master_services) == 2
    assert all(s.master_id == 1 for s in master_services)


def test_add_service():
    """Проверка добавления новой услуги."""
    services = []

    new_service = add_service(
        services, 1, 'Ремонт трубы', 1000.0, 2
    )

    assert len(services) == 1
    assert new_service.id == 1
    assert new_service.master_id == 1
    assert new_service.name == 'Ремонт трубы'
    assert new_service.price == 1000.0
    assert new_service.estimated_hours == 2


def test_calculate_service_cost():
    """Проверка расчёта стоимости услуги."""
    service = {
        'id': 1,
        'master_id': 1,
        'name': 'Замена смесителя',
        'price': 1500.0,
        'duration_hours': 2
    }

    service = Service.from_dict(service)
    total = calculate_service_cost(service, 0.0)
    assert total == 3000.0

    total = calculate_service_cost(service, 10.0)
    assert total == 2700.0

    total = calculate_service_cost(service, 50.0)
    assert total == 1500.0

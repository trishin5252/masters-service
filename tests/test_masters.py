"""Тесты для модуля работы с мастерами."""
from masters import (
    find_master_by_id,
    find_masters_by_specialty,
    sort_masters_by_rating,
    add_master
)


def test_find_master_by_id():
    """Проверка поиска мастера по ID."""
    masters = [
        {
            'id': 1,
            'name': 'Иванов Сергей',
            'specialty': 'Сантехник',
            'rating': 4.8,
            'experience_years': 7
        },
        {
            'id': 2,
            'name': 'Петрова Анна',
            'specialty': 'Электрик',
            'rating': 4.9,
            'experience_years': 5
        }
    ]

    master = find_master_by_id(masters, 1)
    assert master is not None
    assert master['name'] == 'Иванов Сергей'
    assert master['id'] == 1


def test_find_master_by_id_not_found():
    """Проверка поиска несуществующего мастера."""
    masters = [
        {
            'id': 1,
            'name': 'Иванов Сергей',
            'specialty': 'Сантехник',
            'rating': 4.8,
            'experience_years': 7
        }
    ]

    master = find_master_by_id(masters, 999)
    assert master is None


def test_find_masters_by_specialty():
    """Проверка поиска мастеров по специализации."""
    masters = [
        {
            'id': 1,
            'name': 'Иванов Сергей',
            'specialty': 'Сантехник',
            'rating': 4.8,
            'experience_years': 7
        },
        {
            'id': 2,
            'name': 'Петрова Анна',
            'specialty': 'Электрик',
            'rating': 4.9,
            'experience_years': 5
        },
        {
            'id': 3,
            'name': 'Сидоров Петр',
            'specialty': 'Сантехник',
            'rating': 4.5,
            'experience_years': 3
        }
    ]

    found = find_masters_by_specialty(masters, 'сантехник')
    assert len(found) == 2
    assert all(
        m['specialty'].lower() == 'сантехник' for m in found
    )


def test_sort_masters_by_rating():
    """Проверка сортировки мастеров по рейтингу."""
    masters = [
        {
            'id': 1,
            'name': 'Иванов Сергей',
            'specialty': 'Сантехник',
            'rating': 4.8,
            'experience_years': 7
        },
        {
            'id': 2,
            'name': 'Петрова Анна',
            'specialty': 'Электрик',
            'rating': 4.9,
            'experience_years': 5
        },
        {
            'id': 3,
            'name': 'Сидоров Петр',
            'specialty': 'Сантехник',
            'rating': 4.5,
            'experience_years': 3
        }
    ]

    sorted_masters = sort_masters_by_rating(masters)
    assert sorted_masters[0]['rating'] == 4.9
    assert sorted_masters[1]['rating'] == 4.8
    assert sorted_masters[2]['rating'] == 4.5


def test_add_master():
    """Проверка добавления нового мастера."""
    masters = []

    new_master = add_master(
        masters, 'Новиков Иван', 'Сантехник', 4.7, 5
    )

    assert len(masters) == 1
    assert new_master['id'] == 1
    assert new_master['name'] == 'Новиков Иван'
    assert new_master['specialty'] == 'Сантехник'
    assert new_master['rating'] == 4.7
    assert new_master['experience_years'] == 5

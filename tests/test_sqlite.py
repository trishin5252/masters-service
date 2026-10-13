"""Проверки SQL-схемы, импорта и передачи данных на страницы Django."""

import os
import sqlite3

import django
import pytest
from django.test import Client

from db import database, repository
from db.import_json import import_data
from db.queries import all_queries


os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'master_service.settings')
django.setup()


@pytest.fixture
def project_db(tmp_path, monkeypatch):
    monkeypatch.setattr(database, 'DB_PATH', tmp_path / 'project.sqlite')
    counts = import_data()
    assert counts == {'masters': 2, 'users': 2, 'services': 2, 'orders': 1}
    return database.DB_PATH


def test_schema_import_and_foreign_keys(project_db):
    with database.get_connection() as connection:
        names = {row['name'] for row in connection.execute(
            "SELECT name FROM sqlite_master WHERE type='table'"
        )}
        assert {'masters', 'users', 'services', 'orders'} <= names
        references = {row['table'] for row in connection.execute(
            'PRAGMA foreign_key_list(orders)'
        )}
        assert references == {'masters', 'users', 'services'}
        with pytest.raises(sqlite3.IntegrityError):
            connection.execute(
                "INSERT INTO orders VALUES (99, 999, 1, 1, '2026-10-01', 'Создан')"
            )
    assert import_data() == {'masters': 2, 'users': 2, 'services': 2,
                             'orders': 1}


def test_all_named_queries_execute(project_db):
    queries = all_queries()
    assert len(queries) >= 10
    parameters = {
        'master_by_id': (1,),
        'masters_min_rating': (4.5,),
        'services_by_category': ('Сантехника',),
        'orders_on_date': ('2026-10-01',),
        'order_by_id': (1,),
        'master_orders': (1,),
        'popular_masters': (1,),
        'available_masters': ('2026-10-01',),
        'master_busy_on_date': (1, '2026-10-01'),
    }
    with database.get_connection() as connection:
        for name, query in queries.items():
            connection.execute(query, parameters.get(name, ())).fetchall()
    assert len(repository.masters(4.7)) == 1
    assert repository.statistics()['active_orders'] == 1


def test_django_reads_sqlite_and_date_search(project_db):
    client = Client()
    assert 'Петров Алексей Сергеевич' in client.get(
        '/masters/').content.decode('utf-8')
    assert 'Петров Алексей Сергеевич' not in client.get(
        '/masters/available/?date=2026-10-01').content.decode('utf-8')
    assert 'Сидорова Мария Ивановна' in client.get(
        '/masters/available/?date=2026-10-01').content.decode('utf-8')
    assert 'Замена смесителя' in client.get(
        '/orders/1/').content.decode('utf-8')
    assert 'Статистика заказов' in client.get(
        '/orders/statistics/').content.decode('utf-8')

    with database.get_connection() as connection:
        connection.execute("UPDATE masters SET name = 'Тестовый мастер' "
                           'WHERE id = 1')
    assert 'Тестовый мастер' in client.get('/masters/').content.decode('utf-8')

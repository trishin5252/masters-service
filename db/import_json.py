"""Повторяемый перенос исходных данных JSON в SQLite."""

import json
from contextlib import closing

from .database import PROJECT_ROOT, create_schema, get_connection


def read_records(filename):
    path = PROJECT_ROOT / 'data' / filename
    with path.open(encoding='utf-8') as source:
        return json.load(source)


def import_data():
    """Импортировать сущности в порядке их внешних ключей."""
    masters = read_records('masters.json')
    users = read_records('users.json')
    services = read_records('services.json')
    orders = read_records('orders.json')

    with closing(get_connection()) as connection:
        create_schema(connection)
        with connection:
            connection.executemany(
                'INSERT INTO masters '
                '(id, name, specialty, experience, rating, price_per_hour) '
                'VALUES (?, ?, ?, ?, ?, ?) ON CONFLICT(id) DO UPDATE SET '
                'name=excluded.name, specialty=excluded.specialty, '
                'experience=excluded.experience, rating=excluded.rating, '
                'price_per_hour=excluded.price_per_hour',
                [(item['id'], item['name'], item['specialty'],
                  item['experience'], item['rating'], item['price_per_hour'])
                 for item in masters],
            )
            connection.executemany(
                'INSERT INTO users (id, name, role, phone) VALUES (?, ?, ?, ?) '
                'ON CONFLICT(id) DO UPDATE SET name=excluded.name, '
                'role=excluded.role, phone=excluded.phone',
                [(item['id'], item['name'], item.get('role', 'Клиент'),
                  item.get('phone', '')) for item in users],
            )
            connection.executemany(
                'INSERT INTO services '
                '(id, name, category, estimated_hours, master_id, price) '
                'VALUES (?, ?, ?, ?, ?, ?) ON CONFLICT(id) DO UPDATE SET '
                'name=excluded.name, category=excluded.category, '
                'estimated_hours=excluded.estimated_hours, '
                'master_id=excluded.master_id, price=excluded.price',
                [(item['id'], item['name'], item.get('category', ''),
                  item.get('estimated_hours', item.get('duration_hours', 1)),
                  item.get('master_id') or None, item.get('price', 0))
                 for item in services],
            )
            connection.executemany(
                'INSERT INTO orders '
                '(id, master_id, user_id, service_id, booking_date, status) '
                'VALUES (?, ?, ?, ?, ?, ?) ON CONFLICT(id) DO UPDATE SET '
                'master_id=excluded.master_id, user_id=excluded.user_id, '
                'service_id=excluded.service_id, '
                'booking_date=excluded.booking_date, status=excluded.status',
                [(item['id'], item['master_id'], item['user_id'],
                  item['service_id'], item['booking_date'],
                  item.get('status', 'Создан')) for item in orders],
            )
            connection.commit()
        return {
            name: connection.execute(
                'SELECT COUNT(*) FROM ' + name  # Fixed names, not user input.
            ).fetchone()[0]
            for name in ('masters', 'users', 'services', 'orders')
        }


if __name__ == '__main__':
    # Запуск из корня проекта: python -m db.import_json
    print(import_data())

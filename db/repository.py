"""SQL-выборки для Django без дублирования предметных моделей."""

from contextlib import closing
from datetime import date

from models.master import Master
from models.order import Order
from models.service import Service
from models.user import User

from .database import get_connection
from .queries import sql


def rows(name, parameters=()):
    """Выполнить именованный запрос и вернуть строки sqlite3.Row."""
    with closing(get_connection()) as connection:
        return connection.execute(sql(name), parameters).fetchall()


def one(name, parameters=()):
    with closing(get_connection()) as connection:
        return connection.execute(sql(name), parameters).fetchone()


def masters(min_rating=None):
    if min_rating is None:
        result = rows('masters_list')
    else:
        result = rows('masters_min_rating', (min_rating,))
    return [Master.from_dict(dict(row)) for row in result]


def master_by_id(master_id):
    row = one('master_by_id', (master_id,))
    return Master.from_dict(dict(row)) if row else None


def available_masters(booking_date):
    result = rows('available_masters', (booking_date.isoformat(),))
    return [Master.from_dict(dict(row)) for row in result]


def master_available(master_id, booking_date):
    return one('master_busy_on_date',
               (master_id, booking_date.isoformat()))['busy'] == 0


def master_orders(master_id):
    return [dict(row) for row in rows('master_orders', (master_id,))]


def services(category=None):
    if category:
        result = rows('services_by_category', (category,))
    else:
        result = rows('services_list')
    return [Service.from_dict(dict(row)) for row in result]


def service_categories():
    return [row['category'] for row in rows('service_categories')]


def _order_from_row(row):
    master = Master(row['master_id'], row['master_name'], row['specialty'],
                    row['experience'], row['rating'], row['price_per_hour'])
    user = User(row['user_id'], row['user_name'], row['role'], row['phone'])
    service = Service(row['service_id'], row['service_name'], row['category'],
                      row['estimated_hours'], row['service_master_id'] or 0,
                      row['price'])
    return Order(row['id'], master, user, service,
                 date.fromisoformat(row['booking_date']), row['status'])


def orders():
    return [_order_from_row(row) for row in rows('orders_joined')]


def order_by_id(order_id):
    row = one('order_by_id', (order_id,))
    return _order_from_row(row) if row else None


def statistics():
    return {
        'active_orders': one('total_orders')['total'],
        'average_rating': one('average_rating')['average_rating'],
        'by_master': [dict(row) for row in rows('orders_by_master')],
        'by_service': [dict(row) for row in rows('orders_by_service')],
    }

from datetime import date

from masters import Master
from users import User
from orders import cancel_order, create_order, find_orders_by_master
from orders import get_order_statistics, is_master_available


def test_create_order():
    orders = []
    order = create_order(orders, Master(1, 'М', 'С', 1, 4.0, 1), User(1, 'Анна'), 'Анна', 'Замена смесителя', date(2026, 9, 20))
    assert order['id'] == 1
    assert order['status'] == 'Создан'


def test_find_orders_by_master():
    orders = []
    create_order(orders, Master(1, 'М', 'С', 1, 4.0, 1), User(1, 'Анна'), 'Анна', 'Замена смесителя', date(2026, 9, 20))
    create_order(orders, Master(2, 'М2', 'С', 1, 4.0, 1), User(2, 'Иван'), 'Иван', 'Установка розетки', date(2026, 9, 21))
    assert len(find_orders_by_master(orders, 1)) == 1


def test_cancel_order():
    orders = []
    create_order(orders, Master(1, 'М', 'С', 1, 4.0, 1), User(1, 'Анна'), 'Анна', 'Замена смесителя', date(2026, 9, 20))
    assert cancel_order(orders, 1)
    assert orders[0]['status'] == 'Отменён'


def test_master_availability_and_statistics():
    orders = []
    create_order(orders, Master(1, 'М', 'С', 1, 4.0, 1), User(1, 'Анна'), 'Анна', 'Замена смесителя', date(2026, 9, 20))
    assert not is_master_available(orders, 1, date(2026, 9, 20))
    assert get_order_statistics(orders)['Создано'] == 1

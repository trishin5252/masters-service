"""Операции над коллекцией заказов."""

from datetime import date
from typing import Dict, List

from models.master import Master
from models.order import Order
from models.service import Service
from models.user import User


def is_master_available(orders: List[Order], master_id: int,
                        booking_date: date) -> bool:
    return not any(order.master.id == master_id
                   and order.booking_date == booking_date
                   and not order.is_cancelled for order in orders)


def create_order(orders: List[Order], master: Master, user: User,
                 service: Service, booking_date: date) -> Order:
    if not is_master_available(orders, master.id, booking_date):
        raise ValueError('Мастер уже занят на указанную дату.')
    order_id = max((order.id for order in orders), default=0) + 1
    order = Order(order_id, master, user, service, booking_date)
    orders.append(order)
    return order


def find_orders_by_master(orders: List[Order], master_id: int) -> List[Order]:
    return [order for order in orders if order.master.id == master_id]


def cancel_order(orders: List[Order], order_id: int) -> bool:
    order = next((item for item in orders if item.id == order_id), None)
    if order is None:
        return False
    order.cancel()
    return True


def get_order_statistics(orders: List[Order]) -> Dict[str, int]:
    return {'Всего': len(orders),
            'Создано': sum(not order.is_cancelled for order in orders),
            'Отменено': sum(order.is_cancelled for order in orders)}

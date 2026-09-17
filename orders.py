"""Класс заказа и функции обработки коллекции заказов."""

from datetime import date
from typing import Any, Dict, List, Optional

from masters import Master
from users import User


class Order:
    """Заказ клиента на услугу мастера."""

    def __init__(self, order_id: int, master: Master, user: Optional[User],
                 client_name: str, service_name: str, booking_date: date,
                 status: str = 'Создан') -> None:
        self.id = order_id
        self.master = master
        self.user = user
        self.client_name = client_name
        self.service_name = service_name
        self.booking_date = booking_date
        self.status = status

    @property
    def is_cancelled(self) -> bool:
        return self.status == 'Отменён'

    def cancel(self) -> None:
        self.status = 'Отменён'

    def __str__(self) -> str:
        return (f"Заказ #{self.id}: {self.service_name} для {self.client_name} "
                f"на {self.booking_date.isoformat()} - {self.status}")

    def to_dict(self) -> Dict[str, Any]:
        return {'id': self.id, 'master_id': self.master.id,
                'user_id': self.user.id if self.user else 0,
                'client_name': self.client_name, 'service_name': self.service_name,
                'booking_date': self.booking_date.isoformat(), 'status': self.status}


def is_master_available(orders: List[Order], master_id: int, booking_date: date) -> bool:
    return not any(order.master.id == master_id
                   and order.booking_date == booking_date
                   and not order.is_cancelled for order in orders)


def create_order(orders: List[Order], master: Master, user: Optional[User],
                 client_name: str, service_name: str, booking_date: date) -> Order:
    if not is_master_available(orders, master.id, booking_date):
        raise ValueError('Мастер уже занят на указанную дату.')
    order_id = max((order.id for order in orders), default=0) + 1
    order = Order(order_id, master, user, client_name, service_name, booking_date)
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


def get_order_status(order: Order) -> str:
    return str(order)

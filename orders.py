"""Модуль для работы с заказами."""
from datetime import date
from typing import Optional


def get_all_orders(orders: list[dict]) -> list[dict]:
    """Вернуть список всех заказов."""
    return orders


def find_order_by_id(orders: list[dict],
                     order_id: int) -> Optional[dict]:
    """Найти заказ по ID."""
    for order in orders:
        if order['id'] == order_id:
            return order
    return None


def get_orders_by_client(orders: list[dict],
                         client_name: str) -> list[dict]:
    """Получить заказы клиента по имени."""
    return [o for o in orders
            if o['client_name'].lower() == client_name.lower()]


def create_order(orders: list[dict], client_name: str,
                 client_phone: str, master_id: int,
                 service_id: int, order_date: date) -> dict:
    """Создать новый заказ."""
    new_id = max((o['id'] for o in orders), default=0) + 1
    new_order = {
        'id': new_id,
        'client_name': client_name,
        'client_phone': client_phone,
        'master_id': master_id,
        'service_id': service_id,
        'order_date': order_date.isoformat(),
        'status': 'ожидает подтверждения'
    }
    orders.append(new_order)
    return new_order


def cancel_order(orders: list[dict], order_id: int) -> bool:
    """Отменить заказ."""
    order = find_order_by_id(orders, order_id)
    if order:
        order['status'] = 'отменён'
        return True
    return False


def get_order_status(order: dict) -> str:
    """Получить текстовый статус заказа."""
    return f"Заказ #{order['id']}: {order['status']}"


def format_order(order: dict) -> str:
    """Отформатировать информацию о заказе."""
    return (f"Заказ #{order['id']}\n"
            f"Клиент: {order['client_name']}\n"
            f"Телефон: {order['client_phone']}\n"
            f"Мастер ID: {order['master_id']}\n"
            f"Услуга ID: {order['service_id']}\n"
            f"Дата: {order['order_date']}\n"
            f"Статус: {order['status']}")

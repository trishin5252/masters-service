from typing import List, Dict, Any
from datetime import date


def create_order(orders: List[Dict[str, Any]], 
                 master_id: int, 
                 client_name: str, 
                 service_name: str,
                 booking_date: date) -> Dict[str, Any]:
    """Создать новый заказ."""
    order_id = max([order['id'] for order in orders], default=0) + 1
    
    order = {
        'id': order_id,
        'master_id': master_id,
        'client_name': client_name,
        'service_name': service_name,
        'booking_date': booking_date.isoformat(),
        'status': 'Создан'
    }
    
    orders.append(order)
    return order


def find_orders_by_master(orders: List[Dict[str, Any]], master_id: int) -> List[Dict[str, Any]]:
    """Найти все заказы мастера."""
    return [order for order in orders if order['master_id'] == master_id]


def cancel_order(orders: List[Dict[str, Any]], order_id: int) -> bool:
    """Отменить заказ по ID. Возвращает True если успешно."""
    for order in orders:
        if order['id'] == order_id:
            order['status'] = 'Отменён'
            return True
    return False


def get_order_status(order: Dict[str, Any]) -> str:
    """Вернуть текстовый статус заказа."""
    return f"Заказ #{order['id']}: {order['service_name']} - {order['status']}"
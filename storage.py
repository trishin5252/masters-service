import json
from typing import List, Dict, Any
from datetime import date

from masters import Master
from users import User
from orders import Order


def load_json(filename: str) -> List[Dict[str, Any]]:
    """Загрузить данные из JSON файла."""
    try:
        with open(filename, 'r', encoding='utf-8') as file:
            return json.load(file)
    except FileNotFoundError:
        print(f"Файл {filename} не найден. Создаётся новый.")
        return []
    except json.JSONDecodeError:
        print(f"Ошибка чтения {filename}. Возвращается пустой список.")
        return []


def save_json(filename: str, data: List[Dict[str, Any]]) -> None:
    """Сохранить данные в JSON файл."""
    try:
        with open(filename, 'w', encoding='utf-8') as file:
            json.dump(data, file, ensure_ascii=False, indent=4)
    except IOError as e:
        print(f"Ошибка записи в файл {filename}: {e}")


def load_masters(filename: str) -> List[Master]:
    return [Master.from_dict(item) for item in load_json(filename)]


def load_users(filename: str) -> List[User]:
    return [User.from_dict(item) for item in load_json(filename)]


def save_objects(filename: str, objects: List[Any]) -> None:
    save_json(filename, [item.to_dict() for item in objects])


def load_orders(filename: str, masters: List[Master], users: List[User]) -> List[Order]:
    orders = []
    for item in load_json(filename):
        master = next((m for m in masters if m.id == item['master_id']), None)
        user = next((u for u in users if u.id == item.get('user_id')), None)
        if master is None:
            continue
        orders.append(Order(item['id'], master, user, item.get('client_name', ''),
                            item['service_name'], date.fromisoformat(item['booking_date']),
                            item.get('status', 'Создан')))
    return orders

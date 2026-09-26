import json
from typing import List, Dict, Any
from datetime import date
from pathlib import Path

from models.master import Master
from models.order import Order
from models.service import Service
from models.user import User
from operations.user_actions import add_user


def data_path(filename: str) -> Path:
    """Относительные пути считаются от каталога проекта."""
    path = Path(filename)
    return path if path.is_absolute() else Path(__file__).parent / path


def load_json(filename: str) -> Any:
    """Загрузить данные из JSON файла."""
    try:
        with data_path(filename).open('r', encoding='utf-8') as file:
            return json.load(file)
    except FileNotFoundError:
        print(f"Файл {filename} не найден. Создаётся новый.")
        return []
    except (json.JSONDecodeError, UnicodeError) as error:
        raise ValueError(f'Повреждён JSON-файл {filename}') from error


def save_json(filename: str, data: List[Dict[str, Any]]) -> None:
    """Сохранить данные в JSON файл."""
    path = data_path(filename)
    text = json.dumps(data, ensure_ascii=False, indent=4)
    temporary = path.with_suffix('.json.tmp')
    with temporary.open('w', encoding='utf-8') as file:
        file.write(text)
    temporary.replace(path)


def load_masters(filename: str) -> List[Master]:
    return [Master.from_dict(item) for item in load_json(filename)]


def load_users(filename: str) -> List[User]:
    return [User.from_dict(item) for item in load_json(filename)]


def load_services(filename: str) -> List[Service]:
    return [Service.from_dict(item) for item in load_json(filename)]


def save_objects(filename: str, objects: List[Any]) -> None:
    save_json(filename, [item.to_dict() for item in objects])


def load_orders(filename: str, masters: List[Master], users: List[User],
                services: List[Service]) -> List[Order]:
    """Загрузить заказы и восстановить связи с мастером, клиентом и услугой."""
    orders = []
    for item in load_json(filename):
        master = next((m for m in masters if m.id == item['master_id']), None)
        user = next((u for u in users if u.id == item.get('user_id')), None)
        service = next((s for s in services if s.id == item.get('service_id')), None)
        if master is None:
            raise ValueError(f"Заказ {item['id']}: мастер не найден.")
        if user is None:
            if item.get('user_id'):
                raise ValueError(f"Заказ {item['id']}: клиент не найден.")
            user = add_user(users, item.get('client_name', ''))
        if service is None:
            service = next((s for s in services
                            if s.name == item.get('service_name')), None)
        if service is None:
            raise ValueError(f"Заказ {item['id']}: услуга не найдена.")
        orders.append(Order(item['id'], master, user, service,
                            date.fromisoformat(item['booking_date']),
                            item.get('status', 'Создан')))
    return orders

"""Модель заказа."""

from datetime import date
from typing import Any, Dict

from .master import Master
from .service import Service
from .user import User


class Order:
    """Заказ клиента на услугу конкретного мастера."""

    def __init__(self, order_id: int, master: Master, user: User,
                 service: Service, booking_date: date,
                 status: str = 'Создан') -> None:
        if not isinstance(master, Master) or not isinstance(user, User):
            raise ValueError('Заказ должен быть связан с мастером и клиентом.')
        if not isinstance(service, Service):
            raise ValueError('Заказ должен содержать услугу из каталога.')
        if order_id <= 0 or not isinstance(booking_date, date):
            raise ValueError('Укажите положительный ID и корректную дату заказа.')
        if status not in ('Создан', 'Отменён'):
            raise ValueError('Неизвестный статус заказа.')
        self.id = order_id
        self.master = master
        self.user = user
        self.service = service
        self.booking_date = booking_date
        self._status = status

    @property
    def status(self) -> str:
        """Состояние меняется через метод cancel()."""
        return self._status

    @property
    def is_cancelled(self) -> bool:
        return self.status == 'Отменён'

    def cancel(self) -> None:
        self._status = 'Отменён'

    def __str__(self) -> str:
        return (f"Заказ #{self.id}: {self.service.name} для {self.user.name} "
                f"на {self.booking_date.isoformat()} — {self.status}")

    def to_dict(self) -> Dict[str, Any]:
        return {'id': self.id, 'master_id': self.master.id,
                'user_id': self.user.id, 'service_id': self.service.id,
                'booking_date': self.booking_date.isoformat(),
                'status': self.status}

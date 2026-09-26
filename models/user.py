"""Модель пользователя сервиса."""

from typing import Any, Dict


class User:
    """Клиент сервиса."""

    def __init__(self, user_id: int, name: str, role: str = 'Клиент',
                 phone: str = '') -> None:
        if user_id <= 0 or not name.strip():
            raise ValueError('У пользователя должны быть положительный ID и имя.')
        self.id = user_id
        self.name = name
        self.role = role
        self.phone = phone

    def __str__(self) -> str:
        return f"#{self.id} {self.name} ({self.role})"

    def to_dict(self) -> Dict[str, Any]:
        return self.__dict__.copy()

    @classmethod
    def from_dict(cls, data: Dict[str, Any]) -> 'User':
        return cls(data['id'], data['name'], data.get('role', 'Клиент'),
                   data.get('phone', ''))

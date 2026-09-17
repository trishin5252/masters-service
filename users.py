"""Класс пользователя и функции обработки пользователей."""

from typing import Any, Dict, List, Optional


class User:
    """Клиент сервиса."""

    def __init__(self, user_id: int, name: str, role: str = 'Клиент',
                 phone: str = '') -> None:
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


def find_user_by_id(users: List[User], user_id: int) -> Optional[User]:
    return next((user for user in users if user.id == user_id), None)


def get_user_info(user: User) -> str:
    return str(user)


def next_user_id(users: List[User]) -> int:
    return max((user.id for user in users), default=0) + 1

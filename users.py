"""Функции обработки коллекции пользователей."""

from typing import List, Optional

from models.user import User


def find_user_by_id(users: List[User], user_id: int) -> Optional[User]:
    return next((user for user in users if user.id == user_id), None)


def next_user_id(users: List[User]) -> int:
    return max((user.id for user in users), default=0) + 1


def add_user(users: List[User], name: str, phone: str = '') -> User:
    """Создать клиента и добавить его в коллекцию."""
    user = User(next_user_id(users), name.strip(), phone=phone.strip())
    users.append(user)
    return user

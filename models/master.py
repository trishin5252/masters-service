"""Модель мастера."""

from typing import Any, Dict


class Master:
    """Исполнитель услуги."""

    def __init__(self, master_id: int, name: str, specialty: str,
                 experience: int, rating: float, price_per_hour: int) -> None:
        self.id = master_id
        self.name = name
        self.specialty = specialty
        self.experience = experience
        self.rating = rating
        self.price_per_hour = price_per_hour

    def __str__(self) -> str:
        return (f"Мастер #{self.id}: {self.name}\n"
                f"  Специальность: {self.specialty}\n"
                f"  Опыт: {self.experience} лет\n"
                f"  Рейтинг: {self.rating}\n"
                f"  Цена за час: {self.price_per_hour} руб.")

    def to_dict(self) -> Dict[str, Any]:
        return self.__dict__.copy()

    def meets_rating(self, minimum: float) -> bool:
        """Проверить соответствие мастера минимальному рейтингу."""
        return self.rating >= minimum

    @classmethod
    def from_dict(cls, data: Dict[str, Any]) -> 'Master':
        return cls(data['id'], data['name'], data['specialty'],
                   data['experience'], data['rating'], data['price_per_hour'])

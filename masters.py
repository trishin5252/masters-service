"""Класс мастера и функции обработки коллекции мастеров."""

from typing import Any, Dict, List, Optional


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
        return (f"Мастер: {self.name}\n"
                f"  Специальность: {self.specialty}\n"
                f"  Опыт: {self.experience} лет\n"
                f"  Рейтинг: {self.rating}\n"
                f"  Цена за час: {self.price_per_hour} руб.")

    def to_dict(self) -> Dict[str, Any]:
        return self.__dict__.copy()

    @classmethod
    def from_dict(cls, data: Dict[str, Any]) -> 'Master':
        return cls(data['id'], data['name'], data['specialty'],
                   data['experience'], data['rating'], data['price_per_hour'])


def find_master_by_id(masters: List[Master], master_id: int) -> Optional[Master]:
    return next((master for master in masters if master.id == master_id), None)


def find_masters_by_specialty(masters: List[Master], specialty: str) -> List[Master]:
    return [master for master in masters if specialty.lower() in master.specialty.lower()]


def filter_masters_by_rating(masters: List[Master], min_rating: float) -> List[Master]:
    return [master for master in masters if master.rating >= min_rating]


def sort_masters_by_rating(masters: List[Master]) -> List[Master]:
    return sorted(masters, key=lambda master: master.rating, reverse=True)


def get_master_info(master: Master) -> str:
    return str(master)

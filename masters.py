"""Функции обработки коллекции мастеров."""

from typing import List, Optional

from models.master import Master


def find_master_by_id(masters: List[Master], master_id: int) -> Optional[Master]:
    return next((master for master in masters if master.id == master_id), None)


def find_masters_by_specialty(masters: List[Master], specialty: str) -> List[Master]:
    return [master for master in masters if specialty.lower() in master.specialty.lower()]


def filter_masters_by_rating(masters: List[Master], min_rating: float) -> List[Master]:
    return [master for master in masters if master.meets_rating(min_rating)]


def sort_masters_by_rating(masters: List[Master]) -> List[Master]:
    return sorted(masters, key=lambda master: master.rating, reverse=True)

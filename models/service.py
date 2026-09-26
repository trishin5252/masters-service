"""Модель услуги из каталога."""


class Service:
    """Услуга из каталога; поддерживает оба формата данных ПР2."""

    def __init__(self, service_id: int, name: str, category: str = '',
                 estimated_hours: float = 1, master_id: int = 0,
                 price: float = 0) -> None:
        if service_id <= 0 or not name.strip() or estimated_hours <= 0:
            raise ValueError('Некорректные данные услуги.')
        self.id = service_id
        self.name = name
        self.category = category
        self.estimated_hours = estimated_hours
        self.master_id = master_id
        self.price = price

    def calculate_cost(self, discount: float = 0) -> float:
        """Стоимость работы с процентной скидкой."""
        if not 0 <= discount <= 100:
            raise ValueError('Скидка должна быть от 0 до 100.')
        return self.price * self.estimated_hours * (1 - discount / 100)

    def __str__(self) -> str:
        return (f'#{self.id} {self.name}, {self.category}, '
                f'{self.estimated_hours} ч., {self.price} руб./ч')

    def to_dict(self) -> dict:
        return self.__dict__.copy()

    @classmethod
    def from_dict(cls, data: dict) -> 'Service':
        return cls(data['id'], data['name'], data.get('category', ''),
                   data.get('estimated_hours', data.get('duration_hours', 1)),
                   data.get('master_id', 0), data.get('price', 0))

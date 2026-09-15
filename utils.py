"""Вспомогательные функции для ввода и форматирования."""
from datetime import date


def input_int(prompt: str) -> int:
    """Запросить у пользователя целое число."""
    while True:
        try:
            value = int(input(prompt))
            return value
        except ValueError:
            print("Ошибка: введите корректное целое число.")


def input_float(prompt: str) -> float:
    """Запросить у пользователя число с плавающей точкой."""
    while True:
        try:
            value = float(input(prompt))
            return value
        except ValueError:
            print("Ошибка: введите корректное число.")


def input_date(prompt: str) -> date:
    """Запросить у пользователя дату в формате ДД.ММ.ГГГГ."""
    while True:
        try:
            date_str = input(prompt)
            day, month, year = map(int, date_str.split('.'))
            return date(year, month, day)
        except (ValueError, IndexError):
            print("Ошибка: введите дату в формате ДД.ММ.ГГГГ")


def format_date(d: date) -> str:
    """Отформатировать дату в строку ДД.ММ.ГГГГ."""
    return d.strftime("%d.%m.%Y")

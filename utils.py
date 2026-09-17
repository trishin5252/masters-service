from datetime import date
import storage


def input_int(prompt: str) -> int:
    """Запросить целое число у пользователя с обработкой ошибок."""
    while True:
        try:
            value = int(input(prompt))
            return value
        except ValueError:
            print("Ошибка: введите корректное целое число.")


def input_float(prompt: str) -> float:
    """Запросить вещественное число с обработкой ошибок."""
    while True:
        try:
            return float(input(prompt).replace(',', '.'))
        except ValueError:
            print("Ошибка: введите число, например 4.5.")


def input_date(prompt: str) -> date:
    """Запросить дату у пользователя в формате ГГГГ-ММ-ДД."""
    while True:
        try:
            date_str = input(prompt)
            year, month, day = map(int, date_str.split('-'))
            return date(year, month, day)
        except (ValueError, IndexError):
            print("Ошибка: введите дату в формате ГГГГ-ММ-ДД (например, 2026-09-15).")


def show_specialties() -> None:
    """Вывести список доступных специальностей и услуг."""
    specialties = storage.load_json('data/specialties.json')
    
    print("\n=== ДОСТУПНЫЕ СПЕЦИАЛЬНОСТИ И УСЛУГИ ===")
    for category, services in specialties.items():
        print(f"\n{category}:")
        for i, service in enumerate(services, 1):
            print(f"  {i}. {service}")
    print("\n" + "=" * 40)


def show_menu() -> int:
    """Показать главное меню и вернуть выбор пользователя."""
    print("\n=== СЕРВИС ПОИСКА МАСТЕРОВ ===")
    print("1. Показать всех мастеров")
    print("2. Найти мастера по специальности")
    print("3. Найти мастеров с высоким рейтингом")
    print("4. Создать заказ")
    print("5. Показать все заказы")
    print("6. Отменить заказ")
    print("7. Показать пользователей")
    print("8. Показать список специальностей")
    print("9. Показать статистику заказов")
    print("0. Выход")
    
    return input_int("Выберите действие: ")

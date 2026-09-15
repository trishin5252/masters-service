"""
Сервис поиска мастеров.
Начальный сценарий (ПР1).
"""
from datetime import date, timedelta


# Исходные данные (простые типы)
master_name = "Иванов Сергей"
master_specialty = "Сантехник"
master_rating = 4.8
master_experience_years = 7

service_name = "Замена смесителя"
service_price = 1500.0
service_duration_hours = 2

client_name = "Петрова Анна"
client_phone = "+79991234567"

# Дата заказа
order_date = date(2026, 9, 15)


def get_master_info(name: str, specialty: str, rating: float, experience: int) -> str:
    """Сформировать строку с информацией о мастере."""
    return (f"Мастер: {name}\n"
            f"Специализация: {specialty}\n"
            f"Рейтинг: {rating}\n"
            f"Опыт: {experience} лет")


def get_service_info(name: str, price: float, duration: int) -> str:
    """Сформировать строку с информацией об услуге."""
    return (f"Услуга: {name}\n"
            f"Стоимость: {price} руб.\n"
            f"Длительность: {duration} ч.")


def calculate_total_cost(price: float, hours: int, discount_percent: float = 0.0) -> float:
    """Рассчитать итоговую стоимость с учётом скидки."""
    total = price * hours
    discount_amount = total * discount_percent / 100
    return total - discount_amount


def check_master_availability(rating: float, experience: int) -> bool:
    """Проверить, подходит ли мастер для заказа (рейтинг >= 4.0 и опыт >= 3 лет)."""
    if rating >= 4.0 and experience >= 3:
        return True
    return False


def get_order_status(is_confirmed: bool) -> str:
    """Вернуть текстовый статус заказа."""
    if is_confirmed:
        return "Заказ подтверждён мастером"
    return "Заказ ожидает подтверждения"


# Основная логика сценария
if __name__ == "__main__":
    print("=" * 40)
    print("   СЕРВИС ПОИСКА МАСТЕРОВ")
    print("=" * 40)

    # Информация о мастере
    print("\n--- Информация о мастере ---")
    print(get_master_info(master_name, master_specialty,
                          master_rating, master_experience_years))

    # Информация об услуге
    print("\n--- Информация об услуге ---")
    print(get_service_info(service_name, service_price, service_duration_hours))

    # Проверка доступности мастера
    print("\n--- Проверка мастера ---")
    is_available = check_master_availability(master_rating, master_experience_years)
    if is_available:
        print("Мастер подходит для заказа")
    else:
        print("Мастер не соответствует требованиям")

    # Расчёт стоимости
    print("\n--- Расчёт стоимости ---")
    discount = 10.0  # скидка 10%
    total = calculate_total_cost(service_price, service_duration_hours, discount)
    print(f"Базовая цена: {service_price} руб./ч")
    print(f"Длительность: {service_duration_hours} ч.")
    print(f"Скидка: {discount}%")
    print(f"Итого к оплате: {total} руб.")

    # Оформление заказа
    print("\n--- Оформление заказа ---")
    print(f"Клиент: {client_name}")
    print(f"Телефон: {client_phone}")
    print(f"Дата заказа: {order_date}")

    # Статус заказа
    is_confirmed = is_available  # подтверждаем, если мастер подходит
    print(f"Статус: {get_order_status(is_confirmed)}")

    # Прогноз завершения
    if is_confirmed:
        completion_date = order_date + timedelta(hours=service_duration_hours)
        print(f"Ожидаемое завершение: {completion_date}")

    print("\n" + "=" * 40)
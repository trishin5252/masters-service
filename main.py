from datetime import date, datetime

# Данные мастера
master_name = "Петров Алексей Сергеевич"
specialty = "Сантехник"
experience = 7
rating = 4.8
price_per_hour = 1500
is_available = True

# Данные заказа
client_name = "Тришин Никита Дмитриевич"
service = "Замена смесителя"
booking_date = date(2026, 9, 15)
booking_time = "14:00"

# Расчёт стоимости
estimated_hours = 2
total_cost = price_per_hour * estimated_hours

# Определение статуса мастера
def get_master_status(is_available, rating):
    if not is_available:
        return "Мастер сейчас занят"
    elif rating >= 4.5:
        return "Мастер свободен и имеет высокий рейтинг"
    elif rating >= 3.5:
        return "Мастер свободен"
    else:
        return "Мастер свободен, но имеет низкий рейтинг"

# Проверка даты записи
today = date.today()
if booking_date < today:
    date_status = "Дата записи в прошлом"
elif booking_date == today:
    date_status = "Запись на сегодня"
else:
    days_until = (booking_date - today).days
    date_status = f"Запись через {days_until} дн."

# Вывод информации
print("СЕРВИС ПОИСКА МАСТЕРОВ")
print(f"Мастер: {master_name}")
print(f"Специальность: {specialty}")
print(f"Опыт: {experience} лет")
print(f"Рейтинг: {rating}")
print(f"Цена за час: {price_per_hour} руб.")
print(f"Статус: {get_master_status(is_available, rating)}")
print(f"Клиент: {client_name}")
print(f"Услуга: {service}")
print(f"Дата: {booking_date}")
print(f"Время: {booking_time}")
print(f"Статус даты: {date_status}")
print(f"Примерная стоимость: {total_cost} руб.")

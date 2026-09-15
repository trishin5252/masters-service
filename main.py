"""Главный модуль приложения. Точка входа."""
from masters import (
    find_master_by_id, find_masters_by_specialty,
    sort_masters_by_rating, format_master
)
from services import (
    find_service_by_id, get_services_by_master,
    calculate_service_cost, format_service
)
from orders import (
    create_order, cancel_order, format_order
)
from storage import load_data, save_data
from utils import input_int, input_float, input_date


MASTERS_FILE = 'data/masters.json'
SERVICES_FILE = 'data/services.json'
ORDERS_FILE = 'data/orders.json'


def show_menu() -> None:
    """Вывести главное меню."""
    print("\n=== СЕРВИС ПОИСКА МАСТЕРОВ ===")
    print("1. Показать всех мастеров")
    print("2. Найти мастера по специализации")
    print("3. Показать услуги мастера")
    print("4. Рассчитать стоимость услуги")
    print("5. Создать заказ")
    print("6. Показать все заказы")
    print("7. Отменить заказ")
    print("0. Выход")


def show_all_masters(masters: list[dict]) -> None:
    """Показать всех мастеров, отсортированных по рейтингу."""
    print("\n--- Все мастера (по рейтингу) ---")
    if not masters:
        print("Мастера не найдены.")
        return

    sorted_masters = sort_masters_by_rating(masters)
    for master in sorted_masters:
        print(format_master(master))
        print("-" * 30)


def find_master_menu(masters: list[dict]) -> None:
    """Меню поиска мастера по специализации."""
    print("\n--- Доступные специализации ---")
    specialties = set(m['specialty'] for m in masters)
    if specialties:
        for i, spec in enumerate(sorted(specialties), 1):
            count = sum(1 for m in masters if m['specialty'] == spec)
            print(f"{i}. {spec} ({count} мастеров)")
    else:
        print("Специализации не найдены.")
        return

    specialty = input("\nВведите специализацию для поиска (или 0 для возврата): ")

    if specialty == '0':
        print("Возврат в главное меню...")
        return

    found = find_masters_by_specialty(masters, specialty)
    if found:
        print(f"\nНайдено мастеров: {len(found)}")
        for master in found:
            print(format_master(master))
            print("-" * 30)
    else:
        print("Мастера не найдены.")


def show_master_services(masters: list[dict], services: list[dict]) -> None:
    """Показать услуги выбранного мастера."""
    master_id = input_int("Введите ID мастера (или 0 для возврата): ")

    if master_id == 0:
        print("Возврат в главное меню...")
        return

    master = find_master_by_id(masters, master_id)
    if not master:
        print("Мастер не найден.")
        return
    print(f"\nУслуги мастера {master['name']}:")
    master_services = get_services_by_master(services, master_id)
    if master_services:
        for service in master_services:
            print(format_service(service))
            print("-" * 30)
    else:
        print("Услуги не найдены.")


def calculate_cost_menu(services: list[dict]) -> None:
    """Меню расчёта стоимости услуги."""
    service_id = input_int("Введите ID услуги (или 0 для возврата): ")

    if service_id == 0:
        print("Возврат в главное меню...")
        return

    service = find_service_by_id(services, service_id)
    if not service:
        print("Услуга не найдена.")
        return
    discount = input_float("Введите скидку (%): ")
    total = calculate_service_cost(service, discount)
    print(f"\nСтоимость '{service['name']}' со скидкой {discount}%: {total} руб.")


def create_order_menu(masters: list[dict], services: list[dict],
                      orders: list[dict]) -> None:
    """Меню создания заказа."""
    print("\n--- Создание заказа (0 для возврата) ---")

    client_name = input("Введите имя клиента: ")
    if client_name == '0':
        print("Возврат в главное меню...")
        return

    client_phone = input("Введите телефон: ")
    if client_phone == '0':
        print("Возврат в главное меню...")
        return

    master_id = input_int("Введите ID мастера: ")
    if master_id == 0:
        print("Возврат в главное меню...")
        return

    service_id = input_int("Введите ID услуги: ")
    if service_id == 0:
        print("Возврат в главное меню...")
        return

    order_date = input_date("Введите дату заказа (ДД.ММ.ГГГГ): ")

    order = create_order(orders, client_name, client_phone,
                         master_id, service_id, order_date)
    print(f"\nЗаказ #{order['id']} создан!")
    print(format_order(order))


def show_all_orders(orders: list[dict]) -> None:
    """Показать все заказы."""
    print("\n--- Все заказы ---")
    if orders:
        for order in orders:
            print(format_order(order))
            print("-" * 30)
    else:
        print("Заказов нет.")


def cancel_order_menu(orders: list[dict]) -> None:
    """Меню отмены заказа."""
    order_id = input_int("Введите ID заказа для отмены (или 0 для возврата): ")

    if order_id == 0:
        print("Возврат в главное меню...")
        return

    if cancel_order(orders, order_id):
        print(f"Заказ #{order_id} отменён.")
    else:
        print("Заказ не найден.")


def main() -> None:
    """Главная функция приложения."""
    masters = load_data(MASTERS_FILE)
    services = load_data(SERVICES_FILE)
    orders = load_data(ORDERS_FILE)

    while True:
        show_menu()
        choice = input("\nВыберите действие: ")

        if choice == '1':
            show_all_masters(masters)
        elif choice == '2':
            find_master_menu(masters)
        elif choice == '3':
            show_master_services(masters, services)
        elif choice == '4':
            calculate_cost_menu(services)
        elif choice == '5':
            create_order_menu(masters, services, orders)
        elif choice == '6':
            show_all_orders(orders)
        elif choice == '7':
            cancel_order_menu(orders)
        elif choice == '0':
            save_data(MASTERS_FILE, masters)
            save_data(SERVICES_FILE, services)
            save_data(ORDERS_FILE, orders)
            print("Данные сохранены. До свидания!")
            break
        else:
            print("Неверный выбор. Попробуйте снова.")


if __name__ == "__main__":
    main()

from typing import List

import storage
import utils
from models.master import Master
from operations import (master_actions, order_actions, service_catalog,
                        user_actions)


def show_all_masters(masters_list: List[Master]) -> None:
    """Вывести информацию обо всех мастерах."""
    if not masters_list:
        print("Список мастеров пуст.")
        return

    print("\n СПИСОК МАСТЕРОВ ")
    for master in masters_list:
        print(master)
        print("-" * 40)


def main() -> None:
    """Главная функция - точка входа в приложение."""
    # Загрузка данных
    try:
        masters_list = storage.load_masters('data/masters.json')
        services_list = storage.load_services('data/services.json')
        users_list = storage.load_users('data/users.json')
        orders_list = storage.load_orders(
            'data/orders.json', masters_list, users_list, services_list)
    except (OSError, ValueError, KeyError, TypeError) as error:
        print(f'Не удалось загрузить данные: {error}')
        return

    while True:
        choice = utils.show_menu()

        if choice == 0:
            # Сохранение данных перед выходом
            try:
                storage.save_objects('data/masters.json', masters_list)
                storage.save_objects('data/services.json', services_list)
                storage.save_objects('data/users.json', users_list)
                storage.save_objects('data/orders.json', orders_list)
            except (OSError, ValueError) as error:
                print(f'Не удалось сохранить данные: {error}')
                continue
            print("Данные сохранены. До свидания!")
            break

        elif choice == 1:
            # Показать всех мастеров
            sorted_masters = master_actions.sort_masters_by_rating(masters_list)
            show_all_masters(sorted_masters)

        elif choice == 2:
            # Поиск мастера по специальности — СНАЧАЛА ПОКАЗЫВАЕМ СПЕЦИАЛЬНОСТИ
            utils.show_specialties()
            specialty = input("\nВведите название специальности (или услуги): ")
            found = master_actions.find_masters_by_specialty(masters_list, specialty)
            if found:
                show_all_masters(found)
            else:
                print("Мастеры не найдены.")

        elif choice == 3:
            # Мастера с высоким рейтингом
            min_rating = utils.input_float("Введите минимальный рейтинг (например, 4.5): ")
            filtered = master_actions.filter_masters_by_rating(masters_list, min_rating)
            if filtered:
                show_all_masters(filtered)
            else:
                print(f"Мастера с рейтингом >= {min_rating} не найдены.")

        elif choice == 4:
            # Создать заказ
            print("\n СОЗДАНИЕ ЗАКАЗА ")
            utils.show_specialties()
            master_id = utils.input_int("Введите ID мастера: ")
            master = master_actions.find_master_by_id(masters_list, master_id)

            if not master:
                print(f"Мастер с ID {master_id} не найден.")
                continue

            for user in users_list:
                print(user)
            user_id = utils.input_int("Введите ID пользователя: ")
            user = user_actions.find_user_by_id(users_list, user_id)
            if user is None:
                print(f"Пользователь с ID {user_id} не найден.")
                continue
            print('\n КАТАЛОГ УСЛУГ ')
            for service in services_list:
                print(service)
            service_id = utils.input_int('Введите ID услуги: ')
            service = service_catalog.find_service_by_id(services_list, service_id)
            if service is None:
                print(f'Услуга с ID {service_id} не найдена.')
                continue
            booking_date = utils.input_date("Введите дату (ГГГГ-ММ-ДД): ")

            try:
                new_order = order_actions.create_order(
                    orders_list, master, user, service, booking_date
                )
            except ValueError as error:
                print(f"Заказ не создан: {error}")
            else:
                print(f"Заказ #{new_order.id} создан!")

        elif choice == 5:
            # Показать все заказы
            if not orders_list:
                print("Заказов пока нет.")
            else:
                print("\n ВСЕ ЗАКАЗЫ ")
                for order in orders_list:
                    print(order)
                    print("-" * 40)

        elif choice == 6:
            # Отменить заказ
            order_id = utils.input_int("Введите ID заказа для отмены: ")
            if order_actions.cancel_order(orders_list, order_id):
                print(f"Заказ #{order_id} отменён.")
            else:
                print(f"Заказ #{order_id} не найден.")

        elif choice == 7:
            print("\n ПОЛЬЗОВАТЕЛИ ")
            for user in users_list:
                print(user)

        elif choice == 8:
            utils.show_specialties()

        elif choice == 9:
            print("\n СТАТИСТИКА ЗАКАЗОВ ")
            for name, count in order_actions.get_order_statistics(orders_list).items():
                print(f"{name}: {count}")

        elif choice == 11:
            for service in services_list:
                print(service)

        elif choice == 10:
            try:
                user = user_actions.add_user(
                    users_list, input('Имя клиента: '), input('Телефон: '))
                print(f'Добавлен пользователь: {user}')
            except ValueError as error:
                print(error)

        else:
            print("Неверный выбор. Попробуйте снова.")


if __name__ == "__main__":
    main()

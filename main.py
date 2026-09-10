from datetime import date
from typing import List, Dict, Any

import masters
import orders
import storage
import utils


def show_all_masters(masters_list: List[Dict[str, Any]]) -> None:
    """Вывести информацию обо всех мастерах."""
    if not masters_list:
        print("Список мастеров пуст.")
        return
    
    print("\n СПИСОК МАСТЕРОВ ")
    for master in masters_list:
        print(masters.get_master_info(master))
        print("-" * 40)


def main() -> None:
    """Главная функция - точка входа в приложение."""
    # Загрузка данных
    masters_list = storage.load_json('data/masters.json')
    services_list = storage.load_json('data/services.json')
    orders_list = storage.load_json('data/orders.json')
    
    while True:
        choice = utils.show_menu()
        
        if choice == 0:
            # Сохранение данных перед выходом
            storage.save_json('data/masters.json', masters_list)
            storage.save_json('data/services.json', services_list)
            storage.save_json('data/orders.json', orders_list)
            print("Данные сохранены. До свидания!")
            break
        
        elif choice == 1:
            # Показать всех мастеров
            sorted_masters = masters.sort_masters_by_rating(masters_list)
            show_all_masters(sorted_masters)
        
        elif choice == 2:
            # Поиск мастера по специальности — СНАЧАЛА ПОКАЗЫВАЕМ СПЕЦИАЛЬНОСТИ
            utils.show_specialties()
            specialty = input("\nВведите название специальности (или услуги): ")
            found = masters.find_masters_by_specialty(masters_list, specialty)
            if found:
                show_all_masters(found)
            else:
                print("Мастеры не найдены.")
        
        elif choice == 3:
            # Мастера с высоким рейтингом
            min_rating = utils.input_int("Введите минимальный рейтинг (например, 4.5): ")
            filtered = masters.filter_masters_by_rating(masters_list, min_rating)
            if filtered:
                show_all_masters(filtered)
            else:
                print(f"Мастера с рейтингом >= {min_rating} не найдены.")
        
        elif choice == 4:
            # Создать заказ
            print("\n СОЗДАНИЕ ЗАКАЗА ")
            utils.show_specialties()
            master_id = utils.input_int("Введите ID мастера: ")
            master = masters.find_master_by_id(masters_list, master_id)
            
            if not master:
                print(f"Мастер с ID {master_id} не найден.")
                continue
            
            client_name = input("Введите ваше имя: ")
            service_name = input("Введите название услуги: ")
            booking_date = utils.input_date("Введите дату (ГГГГ-ММ-ДД): ")
            
            new_order = orders.create_order(
                orders_list, master_id, client_name, service_name, booking_date
            )
            print(f"Заказ #{new_order['id']} создан!")
        
        elif choice == 5:
            # Показать все заказы
            if not orders_list:
                print("Заказов пока нет.")
            else:
                print("\n ВСЕ ЗАКАЗЫ ")
                for order in orders_list:
                    print(orders.get_order_status(order))
                    print("-" * 40)
        
        elif choice == 6:
            # Отменить заказ
            order_id = utils.input_int("Введите ID заказа для отмены: ")
            if orders.cancel_order(orders_list, order_id):
                print(f"Заказ #{order_id} отменён.")
            else:
                print(f"Заказ #{order_id} не найден.")
        
        elif choice == 7:
            # Показать список специальностей
            utils.show_specialties()
        
        else:
            print("Неверный выбор. Попробуйте снова.")


if __name__ == "__main__":
    main()
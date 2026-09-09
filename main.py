from datetime import date, timedelta

# Данные задачи
task_name = "Разработать главную страницу"
priority = "Высокий"
deadline = date(2026, 9, 25)
is_completed = False
assignee = "Тришин Никита Дмитриевич"

# Расчет дней до дедлайна
today = date.today()
days_left = (deadline - today).days

# Функция определения статуса
def get_task_status(days_left, is_completed):
    if is_completed:
        return " Задача выполнена"
    elif days_left < 0:
        return " Просрочена"
    elif days_left <= 3:
        return " Срочно"
    else:
        return " В работе"

# Вывод информации о задаче
print("ИНФОРМАЦИЯ О ЗАДАЧЕ")
print(f"Название: {task_name}")
print(f"Приоритет: {priority}")
print(f"Исполнитель: {assignee}")
print(f"Дедлайн: {deadline}")
print(f"Дней осталось: {days_left}")
print(f"Статус: {get_task_status(days_left, is_completed)}")

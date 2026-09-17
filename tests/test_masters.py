from masters import (Master, filter_masters_by_rating, find_master_by_id,
                     find_masters_by_specialty)


def test_find_master_by_id():
    """Тест поиска мастера по ID."""
    masters_list = [
        Master(1, 'Петров', 'Сантехник', 5, 4.8, 1000),
        Master(2, 'Сидоров', 'Электрик', 3, 4.2, 900)
    ]
    
    master = find_master_by_id(masters_list, 1)
    assert master is not None
    assert master.name == 'Петров'


def test_find_master_not_found():
    """Тест: мастер не найден."""
    masters_list = [Master(1, 'Петров', 'Сантехник', 5, 4.8, 1000)]
    master = find_master_by_id(masters_list, 999)
    assert master is None


def test_find_masters_by_specialty():
    """Тест поиска по специальности."""
    masters_list = [
        Master(1, 'Петров', 'Сантехник', 5, 4.8, 1000),
        Master(2, 'Сидоров', 'Электрик', 3, 4.2, 900)
    ]
    
    found = find_masters_by_specialty(masters_list, 'сантех')
    assert len(found) == 1
    assert found[0].name == 'Петров'


def test_filter_masters_by_rating():
    """Тест фильтрации по рейтингу."""
    masters_list = [
        Master(1, 'Петров', 'Сантехник', 5, 4.8, 1000),
        Master(2, 'Сидоров', 'Электрик', 3, 3.5, 900),
        Master(3, 'Иванов', 'Мастер', 2, 4.9, 800)
    ]
    
    filtered = filter_masters_by_rating(masters_list, 4.5)
    assert len(filtered) == 2

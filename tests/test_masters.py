from masters import find_master_by_id, find_masters_by_specialty, filter_masters_by_rating


def test_find_master_by_id():
    """Тест поиска мастера по ID."""
    masters_list = [
        {'id': 1, 'name': 'Петров', 'specialty': 'Сантехник'},
        {'id': 2, 'name': 'Сидоров', 'specialty': 'Электрик'}
    ]
    
    master = find_master_by_id(masters_list, 1)
    assert master is not None
    assert master['name'] == 'Петров'


def test_find_master_not_found():
    """Тест: мастер не найден."""
    masters_list = [{'id': 1, 'name': 'Петров'}]
    master = find_master_by_id(masters_list, 999)
    assert master is None


def test_find_masters_by_specialty():
    """Тест поиска по специальности."""
    masters_list = [
        {'id': 1, 'name': 'Петров', 'specialty': 'Сантехник'},
        {'id': 2, 'name': 'Сидоров', 'specialty': 'Электрик'}
    ]
    
    found = find_masters_by_specialty(masters_list, 'сантех')
    assert len(found) == 1
    assert found[0]['name'] == 'Петров'


def test_filter_masters_by_rating():
    """Тест фильтрации по рейтингу."""
    masters_list = [
        {'id': 1, 'name': 'Петров', 'rating': 4.8},
        {'id': 2, 'name': 'Сидоров', 'rating': 3.5},
        {'id': 3, 'name': 'Иванов', 'rating': 4.9}
    ]
    
    filtered = filter_masters_by_rating(masters_list, 4.5)
    assert len(filtered) == 2
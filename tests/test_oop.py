"""Проверки взаимодействия объектов, хранения и консольного сценария."""

from datetime import date
from unittest.mock import patch

import pytest

import main
import storage
from masters import Master, sort_masters_by_rating
from orders import create_order, is_master_available
from users import User, add_user


def sample():
    return Master(1, 'Мастер', 'Электрик', 5, 4.8, 1000), User(1, 'Клиент')


def test_duplicate_and_cancel():
    master, user = sample()
    items = []
    day = date(2026, 10, 1)
    order = create_order(items, master, user, user.name, 'Ремонт', day)
    assert order.master is master and order.user is user
    with pytest.raises(ValueError):
        create_order(items, master, user, user.name, 'Монтаж', day)
    assert len(items) == 1
    order.cancel()
    assert is_master_available(items, master.id, day)
    assert create_order(items, master, user, user.name, 'Монтаж', day).id == 2


def test_json_roundtrip(tmp_path):
    master, user = sample()
    items = []
    order = create_order(items, master, user, user.name, 'Ремонт', date.today())
    order.cancel()
    paths = [str(tmp_path / name) for name in ('m.json', 'u.json', 'o.json')]
    for path, values in zip(paths, ([master], [user], items)):
        storage.save_objects(path, values)
    masters = storage.load_masters(paths[0])
    users = storage.load_users(paths[1])
    loaded = storage.load_orders(paths[2], masters, users)
    assert loaded[0].master is masters[0]
    assert loaded[0].user is users[0]
    assert loaded[0].is_cancelled
    assert loaded[0].to_dict() == order.to_dict()


def test_missing_reference_rejected(tmp_path):
    path = str(tmp_path / 'orders.json')
    storage.save_json(path, [{'id': 1, 'master_id': 99, 'user_id': 1}])
    with pytest.raises(ValueError, match='мастер'):
        storage.load_orders(path, [], [User(1, 'Клиент')])


def test_corrupt_json_is_preserved(tmp_path):
    path = tmp_path / 'broken.json'
    path.write_text('{broken', encoding='utf-8')
    with pytest.raises(ValueError):
        storage.load_json(str(path))
    assert path.read_text(encoding='utf-8') == '{broken'


def test_users_and_strings():
    users = []
    user = add_user(users, ' Анна ', '123')
    assert user.name == 'Анна' and user.id == 1
    assert 'Анна' in str(user)
    assert User.from_dict(user.to_dict()).phone == '123'
    with pytest.raises(ValueError):
        add_user(users, ' ')


def test_rating_and_sort():
    master, _ = sample()
    other = Master(2, 'Другой', 'Электрик', 1, 3.5, 500)
    assert master.meets_rating(4.5)
    assert sort_masters_by_rating([other, master]) == [master, other]
    assert 'Мастер' in str(master)


def test_console_create_and_save(tmp_path, monkeypatch, capsys):
    master, user = sample()
    monkeypatch.setattr(storage, 'data_path', lambda name: tmp_path / name.split('/')[-1])
    storage.save_objects('masters.json', [master])
    storage.save_objects('users.json', [user])
    storage.save_json('orders.json', [])
    storage.save_json('services.json', [])
    storage.save_json('specialties.json', {})
    answers = ['4', '1', '1', 'Ремонт', '2026-10-01', '5', '6', '1', '9', '0']
    with patch('builtins.input', side_effect=answers):
        main.main()
    output = capsys.readouterr().out
    assert 'Заказ #1 создан!' in output
    assert 'Данные сохранены' in output
    assert storage.load_orders('orders.json', [master], [user])[0].is_cancelled

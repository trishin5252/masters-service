"""Проверки URL и страниц Django-версии проекта."""

import os

import django
from django.test import Client

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'master_service.settings')
django.setup()


def test_main_pages_return_success():
    """Основные списки должны быть доступны по HTTP."""
    client = Client()
    for url in ('/', '/masters/', '/services/', '/orders/'):
        assert client.get(url).status_code == 200


def test_detail_pages_and_not_found_response():
    """Динамические страницы возвращают объект или понятный HTTP 404."""
    client = Client()
    assert client.get('/masters/1/').status_code == 200
    assert client.get('/orders/1/').status_code == 200
    assert client.get('/masters/999/').status_code == 404
    assert client.get('/orders/999/').status_code == 404

"""Проверки URL и страниц Django-версии проекта."""

import os

import django
from django.contrib.staticfiles import finders
from django.test import Client
from django.test.utils import setup_test_environment
from django.urls import reverse

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'master_service.settings')
django.setup()
setup_test_environment()


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


def test_templates_routes_and_static_assets():
    """Страницы используют шаблоны, имена URL и собственные ресурсы."""
    client = Client()
    home = client.get(reverse('homepage:index'))
    assert 'homepage/index.html' in [t.name for t in home.templates]
    assert 'base.html' in [t.name for t in home.templates]
    assert reverse('masters:detail', args=[1]) == '/masters/1/'
    assert reverse('services:list') == '/services/'
    assert reverse('orders:detail', args=[1]) == '/orders/1/'
    assert finders.find('homepage/css/style.css')
    assert finders.find('homepage/js/main.js')
    assert finders.find('homepage/img/logo.svg')


def test_list_and_detail_pages_render_domain_data():
    """Контекст и дочерние шаблоны показывают существующие объекты."""
    client = Client()
    masters = client.get('/masters/')
    assert 'masters/master_list.html' in [t.name for t in masters.templates]
    assert masters.context['masters']
    detail = client.get('/masters/1/').content.decode('utf-8')
    assert 'Доступен' in detail or 'Занят' in detail
    orders = client.get('/orders/')
    assert 'orders/order_list.html' in [t.name for t in orders.templates]
    assert orders.context['orders']
    assert 'Заказ №1' in client.get('/orders/1/').content.decode('utf-8')

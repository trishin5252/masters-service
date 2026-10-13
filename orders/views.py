"""Страницы заказов."""

from django.http import HttpRequest, HttpResponse
from django.shortcuts import render

import storage


def load_project_orders():
    """Загрузить заказы вместе с объектами, на которые они ссылаются."""
    masters = storage.load_masters('data/masters.json')
    users = storage.load_users('data/users.json')
    services = storage.load_services('data/services.json')
    return storage.load_orders('data/orders.json', masters, users, services)


def orders_list(request: HttpRequest) -> HttpResponse:
    """Передать список заказов из JSON в шаблон."""
    orders = load_project_orders()
    return render(request, 'orders/order_list.html', {'orders': orders})


def order_detail(request: HttpRequest, order_id: int) -> HttpResponse:
    """Передать заказ в шаблон или вернуть страницу 404."""
    order = next((item for item in load_project_orders() if item.id == order_id), None)
    return render(request, 'orders/order_detail.html',
                  {'order': order}, status=404 if order is None else 200)

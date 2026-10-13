"""Страницы заказов."""

from django.http import HttpRequest, HttpResponse
from django.shortcuts import render

from db import repository


def orders_list(request: HttpRequest) -> HttpResponse:
    """Передать связанные данные заказов из SQLite в шаблон."""
    orders = repository.orders()
    return render(request, 'orders/order_list.html', {'orders': orders})


def order_detail(request: HttpRequest, order_id: int) -> HttpResponse:
    """Передать заказ в шаблон или вернуть страницу 404."""
    order = repository.order_by_id(order_id)
    return render(request, 'orders/order_detail.html',
                  {'order': order}, status=404 if order is None else 200)


def statistics(request: HttpRequest) -> HttpResponse:
    """Показать SQL-статистику заказов по мастерам и услугам."""
    return render(request, 'orders/statistics.html',
                  repository.statistics())

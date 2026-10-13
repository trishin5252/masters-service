"""Страницы мастеров и каталога услуг."""

from datetime import date

from django.http import HttpRequest, HttpResponse
from django.shortcuts import render

import storage
from operations.master_actions import find_master_by_id
from operations.order_actions import is_master_available


def masters_list(request: HttpRequest) -> HttpResponse:
    """Передать список мастеров из JSON в шаблон."""
    masters = storage.load_masters('data/masters.json')
    return render(request, 'masters/master_list.html', {'masters': masters})


def master_detail(request: HttpRequest, master_id: int) -> HttpResponse:
    """Передать мастера и его доступность в шаблон или вернуть 404."""
    masters = storage.load_masters('data/masters.json')
    master = find_master_by_id(masters, master_id)
    if master is None:
        return render(request, 'masters/master_detail.html',
                      {'master': None}, status=404)

    users = storage.load_users('data/users.json')
    services = storage.load_services('data/services.json')
    orders = storage.load_orders('data/orders.json', masters, users, services)
    available = is_master_available(orders, master.id, date.today())
    return render(request, 'masters/master_detail.html',
                  {'master': master, 'available': available})


def services_list(request: HttpRequest) -> HttpResponse:
    """Передать каталог услуг из JSON в шаблон."""
    services = storage.load_services('data/services.json')
    return render(request, 'masters/service_list.html',
                  {'services': services})

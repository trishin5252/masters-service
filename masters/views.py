"""Страницы мастеров и каталога услуг."""

from datetime import date

from django.http import HttpRequest, HttpResponse
from django.shortcuts import render

from db import repository


def masters_list(request: HttpRequest) -> HttpResponse:
    """Передать список мастеров из SQLite с поиском по рейтингу."""
    minimum = request.GET.get('min_rating', '').strip()
    try:
        minimum_rating = float(minimum) if minimum else None
        if minimum_rating is not None and not 0 <= minimum_rating <= 5:
            raise ValueError
    except ValueError:
        minimum_rating = None
        minimum = ''
    return render(request, 'masters/master_list.html', {
        'masters': repository.masters(minimum_rating),
        'min_rating': minimum,
    })


def master_detail(request: HttpRequest, master_id: int) -> HttpResponse:
    """Передать мастера и его доступность в шаблон или вернуть 404."""
    master = repository.master_by_id(master_id)
    if master is None:
        return render(request, 'masters/master_detail.html',
                      {'master': None}, status=404)

    available = repository.master_available(master.id, date.today())
    return render(request, 'masters/master_detail.html',
                  {'master': master, 'available': available,
                   'master_orders': repository.master_orders(master.id)})


def services_list(request: HttpRequest) -> HttpResponse:
    """Передать каталог услуг из SQLite в шаблон."""
    category = request.GET.get('category', '').strip()
    return render(request, 'masters/service_list.html',
                  {'services': repository.services(category),
                   'categories': repository.service_categories(),
                   'selected_category': category})


def available_masters(request: HttpRequest) -> HttpResponse:
    """Найти свободных мастеров SQL-запросом на выбранную дату."""
    value = request.GET.get('date', '').strip()
    try:
        selected_date = date.fromisoformat(value) if value else date.today()
    except ValueError:
        selected_date = date.today()
    return render(request, 'masters/available.html', {
        'masters': repository.available_masters(selected_date),
        'selected_date': selected_date,
    })

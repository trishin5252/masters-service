"""Страницы мастеров и каталога услуг."""

from datetime import date

from django.http import HttpRequest, HttpResponse
from django.utils.html import escape

import storage
from homepage.views import page
from operations.master_actions import find_master_by_id
from operations.order_actions import is_master_available


def masters_list(request: HttpRequest) -> HttpResponse:
    """Показать список мастеров из JSON-хранилища."""
    cards = []
    for master in storage.load_masters('data/masters.json'):
        cards.append(f'''
        <div class="col-md-6"><div class="card h-100 shadow-sm"><div class="card-body">
          <h2 class="h4">{escape(master.name)}</h2>
          <p class="mb-1">{escape(master.specialty)}</p>
          <p class="text-muted">Рейтинг: {master.rating} · Опыт: {master.experience} лет</p>
          <a class="btn btn-outline-primary" href="/masters/{master.id}/">Подробнее</a>
        </div></div></div>''')
    content = '<h1 class="mb-4">Мастера</h1><div class="row g-3">' + ''.join(cards) + '</div>'
    return HttpResponse(page('Мастера', content))


def master_detail(request: HttpRequest, master_id: int) -> HttpResponse:
    """Показать карточку мастера или страницу 404."""
    masters = storage.load_masters('data/masters.json')
    master = find_master_by_id(masters, master_id)
    if master is None:
        content = ('<h1 class="text-danger">Мастер не найден</h1>'
                   '<a href="/masters/">К списку мастеров</a>')
        return HttpResponse(page('Мастер не найден', content), status=404)

    users = storage.load_users('data/users.json')
    services = storage.load_services('data/services.json')
    orders = storage.load_orders('data/orders.json', masters, users, services)
    available = is_master_available(orders, master.id, date.today())
    status = 'доступен' if available else 'занят'
    badge = 'bg-success' if available else 'bg-danger'
    content = f'''
    <div class="card shadow-sm"><div class="card-body">
      <h1 class="card-title">{escape(master.name)}</h1>
      <p><strong>Специализация:</strong> {escape(master.specialty)}</p>
      <p><strong>Опыт:</strong> {master.experience} лет</p>
      <p><strong>Рейтинг:</strong> {master.rating}</p>
      <p><strong>Цена за час:</strong> {master.price_per_hour} руб.</p>
      <p>Статус на сегодня: <span class="badge {badge}">{status}</span></p>
      <a class="btn btn-outline-secondary" href="/masters/">К списку мастеров</a>
    </div></div>'''
    return HttpResponse(page(master.name, content))


def services_list(request: HttpRequest) -> HttpResponse:
    """Показать каталог услуг из JSON-хранилища."""
    items = []
    for service in storage.load_services('data/services.json'):
        items.append(f'''
        <li class="list-group-item d-flex justify-content-between align-items-center">
          <span><strong>{escape(service.name)}</strong> · {escape(service.category)}</span>
          <span>{service.estimated_hours} ч.</span>
        </li>''')
    content = '<h1>Каталог услуг</h1><ul class="list-group">' + ''.join(items) + '</ul>'
    return HttpResponse(page('Каталог услуг', content))

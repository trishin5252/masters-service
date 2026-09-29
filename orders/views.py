"""Страницы заказов."""

from django.http import HttpRequest, HttpResponse
from django.utils.html import escape

import storage
from homepage.views import page


def load_project_orders():
    """Загрузить заказы вместе с объектами, на которые они ссылаются."""
    masters = storage.load_masters('data/masters.json')
    users = storage.load_users('data/users.json')
    services = storage.load_services('data/services.json')
    return storage.load_orders('data/orders.json', masters, users, services)


def orders_list(request: HttpRequest) -> HttpResponse:
    """Показать список заказов из JSON-хранилища."""
    items = []
    for order in load_project_orders():
        status = 'отменён' if order.is_cancelled else 'активен'
        badge = 'bg-secondary' if order.is_cancelled else 'bg-success'
        items.append(f'''
        <li class="list-group-item d-flex justify-content-between align-items-center">
          <a href="/orders/{order.id}/">Заказ #{order.id}: {escape(order.service.name)}</a>
          <span class="badge {badge}">{status}</span>
        </li>''')
    if not items:
        items.append('<li class="list-group-item">Заказов пока нет.</li>')
    content = '<h1>Заказы</h1><ul class="list-group">' + ''.join(items) + '</ul>'
    return HttpResponse(page('Заказы', content))


def order_detail(request: HttpRequest, order_id: int) -> HttpResponse:
    """Показать карточку заказа или страницу 404."""
    order = next((item for item in load_project_orders() if item.id == order_id), None)
    if order is None:
        content = ('<h1 class="text-danger">Заказ не найден</h1>'
                   '<a href="/orders/">К списку заказов</a>')
        return HttpResponse(page('Заказ не найден', content), status=404)

    status = 'отменён' if order.is_cancelled else 'активен'
    badge = 'bg-secondary' if order.is_cancelled else 'bg-success'
    content = f'''
    <div class="card shadow-sm"><div class="card-body">
      <h1 class="h3">Заказ #{order.id}</h1>
      <p><strong>Услуга:</strong> {escape(order.service.name)}</p>
      <p><strong>Мастер:</strong> {escape(order.master.name)}</p>
      <p><strong>Клиент:</strong> {escape(order.user.name)}</p>
      <p><strong>Дата:</strong> {order.booking_date.isoformat()}</p>
      <p>Статус: <span class="badge {badge}">{status}</span></p>
      <a class="btn btn-outline-secondary" href="/orders/">К списку заказов</a>
    </div></div>'''
    return HttpResponse(page(f'Заказ #{order.id}', content))

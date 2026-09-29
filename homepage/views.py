"""Главная страница и общий HTML-каркас веб-приложения."""

from django.http import HttpRequest, HttpResponse


def page(title: str, content: str) -> str:
    """Собрать HTML-страницу с общей навигацией и Bootstrap."""
    bootstrap = ('https://cdn.jsdelivr.net/npm/bootstrap@5.3.3/'
                 'dist/css/bootstrap.min.css')
    return f'''<!doctype html>
<html lang="ru">
<head>
  <meta charset="utf-8">
  <meta name="viewport" content="width=device-width, initial-scale=1">
  <title>{title}</title>
  <link rel="stylesheet" href="{bootstrap}">
</head>
<body class="bg-light">
  <nav class="navbar navbar-expand-lg navbar-dark bg-primary mb-4">
    <div class="container">
      <a class="navbar-brand" href="/">Сервис мастеров</a>
      <div class="navbar-nav">
        <a class="nav-link" href="/masters/">Мастера</a>
        <a class="nav-link" href="/services/">Услуги</a>
        <a class="nav-link" href="/orders/">Заказы</a>
      </div>
    </div>
  </nav>
  <main class="container pb-5">{content}</main>
</body>
</html>'''


def index(request: HttpRequest) -> HttpResponse:
    """Вернуть главную страницу проекта."""
    content = '''
    <div class="p-5 mb-4 bg-white rounded-3 shadow-sm">
      <h1 class="display-5">Сервис поиска мастеров</h1>
      <p class="lead">Веб-интерфейс для просмотра мастеров, услуг и заказов.</p>
      <a class="btn btn-primary me-2" href="/masters/">Смотреть мастеров</a>
      <a class="btn btn-outline-primary" href="/orders/">Смотреть заказы</a>
    </div>
    <div class="row g-3">
      <div class="col-md-4"><div class="card h-100"><div class="card-body">
        <h2 class="h4">Мастера</h2><p>Специализации, опыт и рейтинг.</p>
      </div></div></div>
      <div class="col-md-4"><div class="card h-100"><div class="card-body">
        <h2 class="h4">Услуги</h2><p>Каталог доступных работ.</p>
      </div></div></div>
      <div class="col-md-4"><div class="card h-100"><div class="card-body">
        <h2 class="h4">Заказы</h2><p>Связи пользователя, мастера и услуги.</p>
      </div></div></div>
    </div>
    '''
    return HttpResponse(page('Сервис поиска мастеров', content))

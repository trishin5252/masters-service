"""Главная страница веб-приложения."""

from django.http import HttpRequest, HttpResponse
from django.shortcuts import render


def index(request: HttpRequest) -> HttpResponse:
    """Показать главную страницу через шаблон Django."""
    return render(request, 'homepage/index.html')

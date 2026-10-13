"""Именованный маршрут каталога услуг в приложении masters."""

from django.urls import path

from . import views

app_name = 'services'

urlpatterns = [
    path('', views.services_list, name='list'),
]

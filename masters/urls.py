"""Маршруты разделов мастеров и услуг."""

from django.urls import path

from . import views

urlpatterns = [
    path('', views.masters_list, name='masters_list'),
    path('<int:master_id>/', views.master_detail, name='master_detail'),
]

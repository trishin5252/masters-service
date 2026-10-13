"""Маршруты разделов мастеров и услуг."""

from django.urls import path

from . import views

app_name = 'masters'

urlpatterns = [
    path('', views.masters_list, name='list'),
    path('<int:master_id>/', views.master_detail, name='detail'),
]

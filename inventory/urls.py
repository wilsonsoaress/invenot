# inventory/urls.py

from django.urls import path
from . import views

urlpatterns = [
    # --- URLs de Dispositivos (Devices) ---
    path('devices/', views.device_list, name='device_list'),
    path('device/register/', views.register_device, name='register_device'),
    path('device/<int:pk>/edit/', views.device_update, name='device_update'),
    path('device/<int:pk>/delete/', views.device_delete, name='device_delete'),
    # ADICIONE ESTA LINHA QUE ESTAVA FALTANDO
    path('device/<int:pk>/history/', views.device_history, name='device_history'),

    # --- URLs de Clientes (Clients) ---
    path('client/register/', views.register_client, name='register_client'),
    path('client/success/', views.client_success_view, name='client_success_page'),

    # --- URLs de Movimentações (Movements) ---
    path('movements/', views.movement_list, name='movement_list'),
    path('movement/register/', views.register_movement, name='register_movement'),
    path('movement/<int:pk>/edit/', views.movement_update, name='movement_update'),
    path('movement/<int:pk>/delete/', views.movement_delete, name='movement_delete'),

    # --- URLs Genéricas ---
    path('', views.device_list, name='home'),
    path('success/', views.success_view, name='success_page'),
    path('device/<int:pk>/inspect/', views.create_inspection, name='create_inspection'),
]
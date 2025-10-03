# inventory/admin.py

from django.contrib import admin
from .models import Device, Client, Movimentacao, Inspection # Importação corrigida
from simple_history.admin import SimpleHistoryAdmin

@admin.register(Device)
class DeviceAdmin(SimpleHistoryAdmin):
    list_display = ('id', 'device_type', 'brand', 'model', 'service_tag', 'is_new', 'created_at')
    list_filter = ('device_type', 'brand', 'is_new')
    search_fields = ('model', 'service_tag', 'processor', 'observation')
    history_list_display = ['status']

@admin.register(Client)
class ClientAdmin(admin.ModelAdmin):
    list_display = ('name', 'document', 'phone', 'contact_name')
    search_fields = ('name', 'document')

@admin.register(Movimentacao)
class MovimentacaoAdmin(admin.ModelAdmin):
    list_display = ('device', 'client', 'movement_type', 'movement_date')
    list_filter = ('movement_type', 'movement_date')
    autocomplete_fields = ['device', 'client']

# Registrando o novo modelo de Inspeção
@admin.register(Inspection)
class InspectionAdmin(admin.ModelAdmin):
    list_display = ('device', 'inspection_date', 'physical_state', 'has_charger', 'os_installed', 'has_office')
    list_filter = ('inspection_date',)
    autocomplete_fields = ['device']
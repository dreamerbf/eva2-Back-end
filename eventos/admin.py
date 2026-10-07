"""
Registro de Eventos y Sectores en el admin de Django.
"""
from django.contrib import admin
from .models import Evento, Sector


@admin.register(Evento)
class EventoAdmin(admin.ModelAdmin):
    list_display = ('nombre', 'fecha', 'lugar', 'estado', 'organizador')
    list_filter = ('estado', 'fecha')
    search_fields = ('nombre', 'lugar')


@admin.register(Sector)
class SectorAdmin(admin.ModelAdmin):
    list_display = ('nombre', 'evento', 'precio', 'stock')
    list_filter = ('evento',)
    search_fields = ('nombre',)
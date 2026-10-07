"""
Registro de Compra, ItemCompra y Ticket en el admin.
"""
from django.contrib import admin
from .models import Compra, ItemCompra, Ticket


@admin.register(Compra)
class CompraAdmin(admin.ModelAdmin):
    list_display = ('id', 'usuario', 'estado', 'total', 'creado_en', 'pagado_en')
    list_filter = ('estado', 'creado_en')
    search_fields = ('usuario__username',)


@admin.register(ItemCompra)
class ItemCompraAdmin(admin.ModelAdmin):
    list_display = ('id', 'compra', 'evento_nombre', 'sector_nombre', 'cantidad', 'precio_unitario')


@admin.register(Ticket)
class TicketAdmin(admin.ModelAdmin):
    list_display = ('codigo', 'compra', 'sector', 'creado_en')
    search_fields = ('codigo',)
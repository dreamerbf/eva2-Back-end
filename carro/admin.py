"""
Registro de Carro e ItemCarro en el admin.
"""
from django.contrib import admin
from .models import Carro, ItemCarro


@admin.register(Carro)
class CarroAdmin(admin.ModelAdmin):
    list_display = ('id', 'usuario', 'cantidad_items', 'total', 'creado_en')


@admin.register(ItemCarro)
class ItemCarroAdmin(admin.ModelAdmin):
    list_display = ('id', 'carro', 'sector', 'cantidad', 'subtotal')
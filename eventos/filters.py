"""
Filtros con django-filter para eventos y sectores.
Permite filtrar por nombre, fecha, estado y rango de precios.
"""
import django_filters
from .models import Evento, Sector


class EventoFilter(django_filters.FilterSet):
    nombre = django_filters.CharFilter(lookup_expr='icontains')
    fecha_desde = django_filters.DateTimeFilter(field_name='fecha', lookup_expr='gte')
    fecha_hasta = django_filters.DateTimeFilter(field_name='fecha', lookup_expr='lte')
    estado = django_filters.ChoiceFilter(choices=Evento.Estado.choices)

    class Meta:
        model = Evento
        fields = ['nombre', 'estado', 'fecha_desde', 'fecha_hasta', 'lugar']


class SectorFilter(django_filters.FilterSet):
    precio_min = django_filters.NumberFilter(field_name='precio', lookup_expr='gte')
    precio_max = django_filters.NumberFilter(field_name='precio', lookup_expr='lte')
    solo_disponibles = django_filters.BooleanFilter(method='filtrar_disponibles')

    class Meta:
        model = Sector
        fields = ['evento', 'nombre', 'precio_min', 'precio_max']

    def filtrar_disponibles(self, queryset, name, value):
        """Si value=True, devuelve solo sectores con stock > 0."""
        if value:
            return queryset.filter(stock__gt=0)
        return queryset
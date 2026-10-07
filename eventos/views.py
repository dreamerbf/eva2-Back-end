"""
Vistas de la API para Eventos y Sectores.
- Lectura pública (GET).
- Escritura solo Organizador.
- Filtros aplicados en listados.
"""
from rest_framework import viewsets, permissions
from django_filters.rest_framework import DjangoFilterBackend
from rest_framework.filters import SearchFilter, OrderingFilter

from .models import Evento, Sector
from .serializers import EventoSerializer, SectorSerializer
from .filters import EventoFilter, SectorFilter
from usuarios.permissions import LecturaPublicaEscrituraOrganizador


class EventoViewSet(viewsets.ModelViewSet):
    """
    CRUD de Eventos.
    - GET público.
    - POST/PUT/PATCH/DELETE solo Organizador.
    - Filtros por nombre, fecha, estado, lugar.
    """
    queryset = Evento.objects.select_related('organizador').prefetch_related('sectores')
    serializer_class = EventoSerializer
    permission_classes = [LecturaPublicaEscrituraOrganizador]
    filter_backends = [DjangoFilterBackend, SearchFilter, OrderingFilter]
    filterset_class = EventoFilter
    search_fields = ['nombre', 'lugar', 'descripcion']
    ordering_fields = ['fecha', 'nombre']

    def perform_create(self, serializer):
        # El organizador se toma del usuario autenticado
        serializer.save(organizador=self.request.user)


class SectorViewSet(viewsets.ModelViewSet):
    """
    CRUD de Sectores. Se pueden filtrar por evento, precio y disponibilidad.
    """
    queryset = Sector.objects.select_related('evento')
    serializer_class = SectorSerializer
    permission_classes = [LecturaPublicaEscrituraOrganizador]
    filter_backends = [DjangoFilterBackend, SearchFilter, OrderingFilter]
    filterset_class = SectorFilter
    search_fields = ['nombre', 'evento__nombre']
    ordering_fields = ['precio', 'stock']
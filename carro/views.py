"""
Vistas del carro. Requieren autenticación.
El carro se crea automáticamente al primer acceso.
"""
from rest_framework import viewsets, permissions, status
from rest_framework.decorators import action
from rest_framework.response import Response

from .models import Carro, ItemCarro
from .serializers import CarroSerializer, ItemCarroSerializer


class CarroViewSet(viewsets.ViewSet):
    """
    Endpoints del carro:
    - GET /api/carro/ -> ver carro actual.
    - POST /api/carro/items/ -> agregar ítem.
    - DELETE /api/carro/items/{id}/ -> eliminar ítem.
    - DELETE /api/carro/vaciar/ -> vaciar carro.
    """
    permission_classes = [permissions.IsAuthenticated]

    def _get_carro(self, request):
        """Obtiene o crea el carro del usuario autenticado."""
        carro, _ = Carro.objects.get_or_create(usuario=request.user)
        return carro

    def list(self, request):
        carro = self._get_carro(request)
        serializer = CarroSerializer(carro)
        return Response(serializer.data)

    @action(detail=False, methods=['post'], url_path='items')
    def agregar_item(self, request):
        """Agrega un sector al carro o incrementa su cantidad."""
        carro = self._get_carro(request)
        sector_id = request.data.get('sector')
        cantidad = int(request.data.get('cantidad', 1))

        if not sector_id:
            return Response(
                {'error': 'Debe indicar el sector.'},
                status=status.HTTP_400_BAD_REQUEST,
            )

        # Si ya existe el ítem, se suma la cantidad
        item, creado = ItemCarro.objects.get_or_create(
            carro=carro,
            sector_id=sector_id,
            defaults={'cantidad': cantidad},
        )
        if not creado:
            item.cantidad += cantidad
            item.save()

        serializer = ItemCarroSerializer(item)
        return Response(serializer.data, status=status.HTTP_201_CREATED)

    @action(detail=False, methods=['delete'], url_path='items/(?P<item_id>[^/.]+)')
    def eliminar_item(self, request, item_id=None):
        carro = self._get_carro(request)
        try:
            item = carro.items.get(id=item_id)
            item.delete()
            return Response(status=status.HTTP_204_NO_CONTENT)
        except ItemCarro.DoesNotExist:
            return Response(
                {'error': 'Ítem no encontrado.'},
                status=status.HTTP_404_NOT_FOUND,
            )

    @action(detail=False, methods=['delete'], url_path='vaciar')
    def vaciar(self, request):
        carro = self._get_carro(request)
        carro.items.all().delete()
        return Response(status=status.HTTP_204_NO_CONTENT)
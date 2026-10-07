from rest_framework import serializers
from .models import Carro, ItemCarro
from eventos.serializers import SectorSerializer


class ItemCarroSerializer(serializers.ModelSerializer):
    sector_detalle = SectorSerializer(source='sector', read_only=True)
    subtotal = serializers.DecimalField(max_digits=10, decimal_places=2, read_only=True)

    class Meta:
        model = ItemCarro
        fields = ['id', 'sector', 'sector_detalle', 'cantidad', 'subtotal', 'agregado_en']
        read_only_fields = ['id', 'agregado_en']

    def validate(self, data):
        """Valida que la cantidad no exceda el stock del sector."""
        sector = data.get('sector')
        cantidad = data.get('cantidad', 1)
        if sector and cantidad > sector.stock:
            raise serializers.ValidationError(
                f'Stock insuficiente. Disponible: {sector.stock}'
            )
        return data


class CarroSerializer(serializers.ModelSerializer):
    items = ItemCarroSerializer(many=True, read_only=True)
    total = serializers.DecimalField(max_digits=10, decimal_places=2, read_only=True)
    cantidad_items = serializers.IntegerField(read_only=True)
    usuario_username = serializers.CharField(source='usuario.username', read_only=True)

    class Meta:
        model = Carro
        fields = ['id', 'usuario', 'usuario_username', 'items', 'total', 'cantidad_items', 'creado_en']
        read_only_fields = ['id', 'usuario', 'creado_en']
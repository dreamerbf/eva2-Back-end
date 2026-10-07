from rest_framework import serializers
from .models import Evento, Sector


class SectorSerializer(serializers.ModelSerializer):
    evento_nombre = serializers.CharField(source='evento.nombre', read_only=True)

    class Meta:
        model = Sector
        fields = ['id', 'evento', 'evento_nombre', 'nombre', 'precio', 'stock', 'fila']
        read_only_fields = ['id']


class EventoSerializer(serializers.ModelSerializer):
    sectores = SectorSerializer(many=True, read_only=True)
    organizador_username = serializers.CharField(source='organizador.username', read_only=True)

    class Meta:
        model = Evento
        fields = [
            'id', 'nombre', 'descripcion', 'fecha', 'lugar', 'estado',
            'organizador', 'organizador_username', 'sectores',
            'creado_en', 'actualizado_en',
        ]
        read_only_fields = ['id', 'creado_en', 'actualizado_en', 'organizador']
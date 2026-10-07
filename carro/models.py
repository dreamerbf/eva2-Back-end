"""
Carro de compras persistente.
Relación 1:1 con Usuario. Los ítems persisten en PostgreSQL,
por lo que sobreviven al logout y al cambio de dispositivo.
"""
from django.db import models
from django.conf import settings


class Carro(models.Model):
    """
    Carro activo de un usuario. Relación OneToOne.
    """
    usuario = models.OneToOneField(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
        related_name='carro',
    )
    creado_en = models.DateTimeField(auto_now_add=True)
    actualizado_en = models.DateTimeField(auto_now=True)

    class Meta:
        verbose_name = 'Carro'
        verbose_name_plural = 'Carros'

    @property
    def total(self):
        return sum(item.subtotal for item in self.items.all())

    @property
    def cantidad_items(self):
        return self.items.count()

    def __str__(self):
        return f'Carro de {self.usuario.username}'


class ItemCarro(models.Model):
    """
    Ítem dentro del carro: un sector y una cantidad.
    No se permite el mismo sector dos veces (unique_together).
    """
    carro = models.ForeignKey(
        Carro,
        on_delete=models.CASCADE,
        related_name='items',
    )
    sector = models.ForeignKey(
        'eventos.Sector',
        on_delete=models.CASCADE,
    )
    cantidad = models.PositiveIntegerField(default=1)
    agregado_en = models.DateTimeField(auto_now_add=True)

    class Meta:
        unique_together = ('carro', 'sector')
        verbose_name = 'Ítem de Carro'
        verbose_name_plural = 'Ítems de Carro'

    @property
    def subtotal(self):
        return self.sector.precio * self.cantidad

    def __str__(self):
        return f'{self.cantidad} x {self.sector.nombre}'
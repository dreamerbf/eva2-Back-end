"""
Modelos de Compra, ItemCompra y Ticket.

- Compra: cabecera de la orden con estado CHOICES.
- ItemCompra: congela el precio histórico del sector al momento de la compra.
- Ticket: entrada individual con UUID único, generada al pasar a PAGADO.
"""
import uuid
from django.db import models
from django.conf import settings


class Compra(models.Model):
    """
    Orden de compra. Usa CHOICES para el estado.
    Flujo: PENDIENTE -> PAGADO -> ENTREGADO / CANCELADO
    """
    class Estado(models.TextChoices):
        PENDIENTE = 'PENDIENTE', 'Pendiente'
        PAGADO = 'PAGADO', 'Pagado'
        ENTREGADO = 'ENTREGADO', 'Entregado'
        CANCELADO = 'CANCELADO', 'Cancelado'

    usuario = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
        related_name='compras',
    )
    estado = models.CharField(
        max_length=20,
        choices=Estado.choices,
        default=Estado.PENDIENTE,
    )
    total = models.DecimalField(max_digits=12, decimal_places=2, default=0)
    creado_en = models.DateTimeField(auto_now_add=True)
    pagado_en = models.DateTimeField(null=True, blank=True)

    class Meta:
        ordering = ['-creado_en']
        verbose_name = 'Compra'
        verbose_name_plural = 'Compras'

    def __str__(self):
        return f'Compra #{self.id} - {self.usuario.username} ({self.estado})'


class ItemCompra(models.Model):
    """
    Detalle de la compra. Congela el precio del sector al momento
    de la compra, para que cambios futuros no afecten la orden.
    """
    compra = models.ForeignKey(
        Compra,
        on_delete=models.CASCADE,
        related_name='items',
    )
    sector = models.ForeignKey('eventos.Sector', on_delete=models.PROTECT)
    sector_nombre = models.CharField(max_length=100)
    evento_nombre = models.CharField(max_length=200)
    precio_unitario = models.DecimalField(max_digits=10, decimal_places=2)
    cantidad = models.PositiveIntegerField()

    @property
    def subtotal(self):
        return self.precio_unitario * self.cantidad

    def __str__(self):
        return f'{self.cantidad} x {self.sector_nombre}'


class Ticket(models.Model):
    """
    Entrada individual con código UUID único, generada al pagar.
    """
    compra = models.ForeignKey(
        Compra,
        on_delete=models.CASCADE,
        related_name='tickets',
    )
    sector = models.ForeignKey('eventos.Sector', on_delete=models.PROTECT)
    codigo = models.UUIDField(default=uuid.uuid4, unique=True, editable=False)
    creado_en = models.DateTimeField(auto_now_add=True)

    class Meta:
        verbose_name = 'Ticket'
        verbose_name_plural = 'Tickets'

    def __str__(self):
        return f'Ticket {self.codigo}'
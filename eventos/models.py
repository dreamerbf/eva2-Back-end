"""
Modelos de Eventos y Sectores.
Un Evento tiene muchos Sectores (1:N).
Cada Sector maneja stock y precio, y usa CHOICES para el estado del evento.
"""
from django.db import models
from django.utils import timezone


class Evento(models.Model):
    """
    Evento/Concierto. Usa CHOICES para el estado del evento.
    """
    class Estado(models.TextChoices):
        BORRADOR = 'BORRADOR', 'Borrador'
        PUBLICADO = 'PUBLICADO', 'Publicado'
        AGOTADO = 'AGOTADO', 'Agotado'
        CANCELADO = 'CANCELADO', 'Cancelado'
        FINALIZADO = 'FINALIZADO', 'Finalizado'

    nombre = models.CharField(max_length=200)
    descripcion = models.TextField(blank=True)
    fecha = models.DateTimeField()
    lugar = models.CharField(max_length=200)
    estado = models.CharField(
        max_length=20,
        choices=Estado.choices,
        default=Estado.PUBLICADO,
    )
    organizador = models.ForeignKey(
        'usuarios.Usuario',
        on_delete=models.CASCADE,
        related_name='eventos_organizados',
        limit_choices_to={'rol': 'ORGANIZADOR'},
    )
    creado_en = models.DateTimeField(auto_now_add=True)
    actualizado_en = models.DateTimeField(auto_now=True)

    class Meta:
        ordering = ['fecha']
        verbose_name = 'Evento'
        verbose_name_plural = 'Eventos'

    def __str__(self):
        return f'{self.nombre} - {self.fecha:%d/%m/%Y}'


class Sector(models.Model):
    """
    Sector dentro de un evento (ej: VIP, Cancha, Galería).
    Tiene stock (cupos) y precio. El stock se descuenta SOLO al pagar.
    """
    evento = models.ForeignKey(
        Evento,
        on_delete=models.CASCADE,
        related_name='sectores',
    )
    nombre = models.CharField(max_length=100)
    precio = models.DecimalField(max_digits=10, decimal_places=2)
    stock = models.PositiveIntegerField(default=0)
    fila = models.CharField(max_length=10, blank=True, null=True)

    class Meta:
        unique_together = ('evento', 'nombre')
        verbose_name = 'Sector'
        verbose_name_plural = 'Sectores'

    @property
    def disponible(self):
        return self.stock > 0

    def __str__(self):
        return f'{self.evento.nombre} - {self.nombre} (${self.precio})'
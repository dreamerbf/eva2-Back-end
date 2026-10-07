"""
Modelo de Usuario personalizado con campo ROL usando CHOICES.
Esto permite diferenciar entre Espectador y Organizador.
"""
from django.contrib.auth.models import AbstractUser
from django.db import models


class Usuario(AbstractUser):
    """
    Usuario extendido con rol. Se usa CHOICES para restringir
    los valores válidos del campo 'rol'.
    """

    class Rol(models.TextChoices):
        ESPECTADOR = 'ESPECTADOR', 'Espectador'
        ORGANIZADOR = 'ORGANIZADOR', 'Organizador'

    rol = models.CharField(
        max_length=20,
        choices=Rol.choices,
        default=Rol.ESPECTADOR,
        help_text='Rol del usuario dentro del sistema.'
    )
    rut = models.CharField(max_length=12, blank=True, null=True)

    def es_organizador(self):
        return self.rol == self.Rol.ORGANIZADOR

    def es_espectador(self):
        return self.rol == self.Rol.ESPECTADOR

    def __str__(self):
        return f'{self.username} ({self.get_rol_display()})'
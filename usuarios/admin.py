"""
Registro del modelo Usuario en el admin de Django.
Se usa UserAdmin para reutilizar la interfaz de usuario de Django
(gestión de contraseñas, permisos, etc.) y se agregan los campos
personalizados 'rol' y 'rut'.
"""
from django.contrib import admin
from django.contrib.auth.admin import UserAdmin
from .models import Usuario


@admin.register(Usuario)
class UsuarioAdmin(UserAdmin):
    """
    Extiende el UserAdmin estándar para mostrar el campo 'rol' y 'rut'.
    """
    list_display = ('username', 'email', 'first_name', 'last_name', 'rol', 'is_staff')
    list_filter = ('rol', 'is_staff', 'is_superuser', 'is_active')
    search_fields = ('username', 'email', 'rut')

    # Agrega 'rol' y 'rut' a los fieldsets del UserAdmin
    fieldsets = UserAdmin.fieldsets + (
        ('Datos adicionales', {'fields': ('rol', 'rut')}),
    )

    # Agrega 'rol' y 'rut' al formulario de creación
    add_fieldsets = UserAdmin.add_fieldsets + (
        ('Datos adicionales', {'fields': ('rol', 'rut')}),
    )
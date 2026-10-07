"""
Permisos personalizados por rol para usar en las vistas DRF.
"""
from rest_framework.permissions import BasePermission, SAFE_METHODS


class EsOrganizador(BasePermission):
    """Permite acceso solo a usuarios con rol ORGANIZADOR."""
    def has_permission(self, request, view):
        return bool(
            request.user and
            request.user.is_authenticated and
            request.user.rol == 'ORGANIZADOR'
        )


class EsEspectador(BasePermission):
    """Permite acceso solo a usuarios con rol ESPECTADOR."""
    def has_permission(self, request, view):
        return bool(
            request.user and
            request.user.is_authenticated and
            request.user.rol == 'ESPECTADOR'
        )


class LecturaPublicaEscrituraOrganizador(BasePermission):
    """
    GET/HEAD/OPTIONS: público.
    POST/PUT/PATCH/DELETE: solo Organizador.
    """
    def has_permission(self, request, view):
        if request.method in SAFE_METHODS:
            return True
        return bool(
            request.user and
            request.user.is_authenticated and
            request.user.rol == 'ORGANIZADOR'
        )
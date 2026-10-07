"""
Vistas de autenticación (API + HTML) y vistas HTML base
que incluyen el footer con los datos del alumno.
"""
from django.shortcuts import render, redirect
from django.contrib.auth import logout, authenticate, login
from django.views.generic import TemplateView, View
from django.utils.decorators import method_decorator
from django.contrib.auth.decorators import login_required
from rest_framework import generics, permissions, status
from rest_framework.response import Response
from rest_framework_simplejwt.views import TokenObtainPairView

from .models import Usuario
from .serializers import (
    RegistroSerializer,
    UsuarioSerializer,
    CustomTokenObtainPairSerializer,
)


# ============================================================
# API: Registro y Login JWT
# ============================================================
class RegistroAPIView(generics.CreateAPIView):
    """POST /api/registro/ -> crea un usuario nuevo."""
    queryset = Usuario.objects.all()
    serializer_class = RegistroSerializer
    permission_classes = [permissions.AllowAny]


class LoginJWTView(TokenObtainPairView):
    """POST /api/login/ -> devuelve access y refresh con claim 'rol'."""
    serializer_class = CustomTokenObtainPairSerializer
    permission_classes = [permissions.AllowAny]


class PerfilAPIView(generics.RetrieveUpdateAPIView):
    """GET/PUT /api/perfil/ -> datos del usuario autenticado."""
    serializer_class = UsuarioSerializer
    permission_classes = [permissions.IsAuthenticated]

    def get_object(self):
        return self.request.user


# ============================================================
# VISTAS HTML (frontend básico con footer del alumno)
# ============================================================
DATOS_ALUMNO = {
    'alumno_nombre': 'Benjamin Cheuquemilla',
    'alumno_seccion': 'TI3041',
    'alumno_anio': '2026',
}


class LoginHTMLView(View):
    """Vista HTML de login. Si el usuario ya está autenticado, redirige al catálogo."""
    def get(self, request):
        if request.user.is_authenticated:
            return redirect('catalogo')
        return render(request, 'login.html', DATOS_ALUMNO)

    def post(self, request):
        username = request.POST.get('username')
        password = request.POST.get('password')
        user = authenticate(request, username=username, password=password)
        if user is not None:
            login(request, user)
            next_url = request.GET.get('next', 'catalogo')
            return redirect(next_url)
        return render(request, 'login.html', {
            **DATOS_ALUMNO,
            'error': 'Credenciales inválidas'
        })


class RegistroHTMLView(View):
    def get(self, request):
        return render(request, 'registro.html', DATOS_ALUMNO)

    def post(self, request):
        username = request.POST.get('username')
        password = request.POST.get('password')
        email = request.POST.get('email', '')
        rol = request.POST.get('rol', 'ESPECTADOR')
        if Usuario.objects.filter(username=username).exists():
            return render(request, 'registro.html', {
                **DATOS_ALUMNO,
                'error': 'El usuario ya existe'
            })
        user = Usuario.objects.create_user(
            username=username, password=password, email=email, rol=rol
        )
        login(request, user)
        return redirect('catalogo')


def logout_view(request):
    logout(request)
    return redirect('login')


class CatalogoHTMLView(TemplateView):
    """
    Vista HTML del catálogo. Es pública para poder ver los eventos,
    pero al agregar al carro se valida la sesión en el frontend.
    """
    template_name = 'catalogo.html'

    def get_context_data(self, **kwargs):
        ctx = super().get_context_data(**kwargs)
        ctx.update(DATOS_ALUMNO)
        return ctx


@method_decorator(login_required, name='dispatch')
class CarroHTMLView(TemplateView):
    """
    Vista HTML del carro. Requiere login.
    Si no hay sesión, Django redirige a /login/?next=/carro/.
    """
    template_name = 'carro.html'

    def get_context_data(self, **kwargs):
        ctx = super().get_context_data(**kwargs)
        ctx.update(DATOS_ALUMNO)
        return ctx
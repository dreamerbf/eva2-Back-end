"""
URLs raíz. Se sirve la página única en '/' y la API bajo '/api/'.
"""
from django.contrib import admin
from django.urls import path, include
from django.views.generic import TemplateView
from drf_spectacular.views import SpectacularAPIView, SpectacularSwaggerView

urlpatterns = [
    path('admin/', admin.site.urls),

    # Página única (login + catálogo + carro + mis entradas)
    path('', TemplateView.as_view(template_name='index.html'), name='index'),

    # Documentación OpenAPI
    path('api/schema/', SpectacularAPIView.as_view(), name='schema'),
    path('api/docs/', SpectacularSwaggerView.as_view(url_name='schema'), name='swagger-ui'),

    # API
    path('api/', include('usuarios.urls')),
    path('api/', include('eventos.urls')),
    path('api/', include('carro.urls')),
    path('api/', include('compras.urls')),
]
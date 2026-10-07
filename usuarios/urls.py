from django.urls import path
from rest_framework_simplejwt.views import TokenRefreshView
from .views import RegistroAPIView, LoginJWTView, PerfilAPIView

urlpatterns = [
    path('registro/', RegistroAPIView.as_view(), name='api-registro'),
    path('login/', LoginJWTView.as_view(), name='api-login'),
    path('token/refresh/', TokenRefreshView.as_view(), name='api-token-refresh'),
    path('perfil/', PerfilAPIView.as_view(), name='api-perfil'),
]
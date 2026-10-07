from rest_framework.routers import DefaultRouter
from .views import CarroViewSet

router = DefaultRouter()
router.register(r'carro', CarroViewSet, basename='carro')

urlpatterns = router.urls
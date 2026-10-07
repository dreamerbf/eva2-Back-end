from rest_framework.routers import DefaultRouter
from .views import EventoViewSet, SectorViewSet

router = DefaultRouter()
router.register(r'eventos', EventoViewSet, basename='evento')
router.register(r'sectores', SectorViewSet, basename='sector')

urlpatterns = router.urls
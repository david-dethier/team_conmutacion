from rest_framework.routers import DefaultRouter
from .views import DomicilioGeolocalizadoViewSet

router = DefaultRouter()

router.register("domicilios", DomicilioGeolocalizadoViewSet, basename="DomicilioGeolocalizado")

urlpatterns = router.urls

from rest_framework.routers import DefaultRouter
from api.v1.red.views import NodoViewSet

router = DefaultRouter()

router.register(r"", NodoViewSet, basename="Nodos")


urlpatterns = router.urls

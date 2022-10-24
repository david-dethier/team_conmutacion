from rest_framework.routers import DefaultRouter
from api.v1.logins.views import LoginViewSet

router = DefaultRouter()
router.register(
    r"",
    LoginViewSet,
    basename="Login",
)

urlpatterns = router.urls

from rest_framework.routers import DefaultRouter
from api.v1.metrics.views.conexiones import CompletedWorkConnectionViewSet
from api.v1.metrics.views.reclamos import CompletedWorkClaimViewSet
from api.v1.metrics.views.monitoreos import CablemodemCountMonitorViewset
from api.v1.metrics.views.monitoreos import EventoDeNodoViewset, EventoDeNodoEquipoAfectadoViewset
from api.v1.metrics.views.llamadas_tecnicas import LlamadaTecnicaViewSet

router = DefaultRouter()
router.register(
    r"conexiones/completedworks",
    CompletedWorkConnectionViewSet,
    basename="CompletedWorkConexiones",
)
router.register(
    r"reclamos/completedworks",
    CompletedWorkClaimViewSet,
    basename="CompletedWorkReclamos",
)

router.register(
    r"monitoreos/cablemodem/activos",
    CablemodemCountMonitorViewset,
    basename="MonitoreoCablemodemsActivos",
)
router.register(r"llamadas/operador", LlamadaTecnicaViewSet, basename="LlamadasTecnicas")
router.register(r"monitoreos/nodo/eventos", EventoDeNodoViewset, basename="EventoDeNodo")
router.register(r"monitoreos/nodo/equiposafectados", EventoDeNodoEquipoAfectadoViewset, basename="EventoDeNodoEquipoAfectado")


urlpatterns = router.urls

import json
import requests

from rest_framework import viewsets
from rest_framework import status
from rest_framework.response import Response
from rest_framework.exceptions import APIException

from api.v1.metrics import selectors as metrics_selectors
from api.v1.metrics import services
from api.v1.metrics.serializers.monitoreos import (
    CablemodemCountMonitoredSerializer,
    EventoDeNodoEquiposAdectadosSerializer,
    EventoDeNodoSerializer,
)
from api.v1.metrics.models.monitoreos import (
    NodoEventoModel,
    NodoEventoEquipoAfectadoModel,
)

from api.v1.gis import selectors as gis_selectors
from api.v1.gis import servicies as gis_servicies


class CablemodemCountMonitorViewset(viewsets.ReadOnlyModelViewSet):

    serializer_class = CablemodemCountMonitoredSerializer

    def get_queryset(self):

        response = requests.post(
            "https://www.usina.net.ar/mfredes/zabbdroopy/zabbmonitoring.php",
            data='{"action":"count"}',
        )

        if response.status_code == 200:
            active_count = json.loads(response.content.decode("utf-8"))["count"]
            self.queryset = {"active_monitoring": active_count}

        return self.queryset

    def list(self, request):

        active_monitoring = self.get_queryset()
        serializer = CablemodemCountMonitoredSerializer(data=active_monitoring)

        if serializer.is_valid(raise_exception=True):
            return Response(serializer.validated_data)


class EventoDeNodoViewset(viewsets.ReadOnlyModelViewSet):

    serializer_class = EventoDeNodoSerializer
    queryset = NodoEventoModel.objects.prefetch_related("afectados").order_by(
        "-eventid"
    )

    def list(self, request, *args, **kwargs):

        eventos_raw = metrics_selectors.fetch_eventos_de_nodos()

        if eventos_raw["status_code"] != status.HTTP_200_OK:
            raise APIException(code=eventos_raw["status_code"])

        eventids_ignorados = NodoEventoModel.objects.filter(estado="FIN").values_list(
            "eventid", flat=True
        )

        eventos = services.parse_data_evento_de_nodo(eventos_raw, eventids_ignorados)
        for evento in eventos:
            
            evento_model, evento_created = NodoEventoModel.objects.update_or_create(
                eventid=evento["eventid"], defaults=evento
            )

            detalle_evento_raw = metrics_selectors.fetch_detalle_evento_de_nodo(
                evento["eventid"]
            )

            if detalle_evento_raw["status_code"] != status.HTTP_200_OK:
                raise APIException(code=eventos_raw["status_code"])

            detalles = services.parse_data_evento_de_nodo_equipos_afectados(
                detalle_evento_raw
            )

            print(f'Se proceso el evento {evento["eventid"]}')
            for detalle in detalles:
                gis_servicies.geolocalizar(detalle["domicilio"])

                detalle["evento"] = evento_model

                NodoEventoEquipoAfectadoModel.objects.update_or_create(
                    macaddress=detalle["macaddress"],
                    evento=evento_model,
                    defaults=detalle,
                )

        return super().list(request, *args, **kwargs)

    def geolocalizar_domicilio(self, domicilio):
        pass
        # data_domicilio ={
        #     "calle":serializer.validated_data["calle"],
        #     "numero":serializer.validated_data["numero"],
        #     "casa":serializer.validated_data["casa"],
        #     "ciudad":serializer.validated_data["ciudad"],
        # }

        # serializer = DomicilioGeoCodificadoViewSet.serializer_class(data=data_domicilio)
        # vs = DomicilioGeoCodificadoViewSet().create(
        #     request={"data": {"calle": "ALVEAR"}}
        # )
        
        # print(response)
        # endpoint = DomicilioGeoCodificadoViewSet.create()


class EventoDeNodoEquipoAfectadoViewset(viewsets.ReadOnlyModelViewSet):

    serializer_class = EventoDeNodoEquiposAdectadosSerializer
    queryset = NodoEventoEquipoAfectadoModel.objects.select_related("evento")
    filterset_fields = ["evento"]
    search_fields = ["macaddress", "domicilio", "cuenta"]

    def list(self, request, *args, **kwargs):

        return super().list(request, *args, **kwargs)

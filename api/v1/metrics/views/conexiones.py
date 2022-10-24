import json
import requests

from rest_framework import viewsets, mixins
from rest_framework import status
from rest_framework import serializers

from api.v1.metrics.models.conexiones import ConexionesCompletedWorkModel
from api.v1.metrics.models.commons import CuadrillaTecnicaModel
from api.v1.metrics.serializers.conexiones import (
    CompletedWorkConnectionSerializer,
)


URL_COMPLETEDWORKS = "http://192.168.36.36/Recladisticas/estadisConx.php"


class CompletedWorkConnectionViewSet(viewsets.ReadOnlyModelViewSet):

    serializer_class = CompletedWorkConnectionSerializer
    filterset_fields = ["date", "technical_team"]
    search_fields = ["technical_team"]

    def get_queryset(self):

        self.sincronize()
        return ConexionesCompletedWorkModel.objects.all()

    def sincronize(self):
        """Sincroniza la base de datos (creando o actualizando)
        con la respuesta del Request, filtrado por fecha."""

        date_query_param = self.request.query_params.get("date", None)

        if not date_query_param:
            return None, False

        # Paso validacion de parametro "date" pasado por query_param.
        # Comienza la logica de sincronizacion entre la BD y la data del request.
        request_data = requests.get(URL_COMPLETEDWORKS, {"fecha": date_query_param})

        if request_data.content.decode("utf-8") == "":
            return None, False

        json_request_data = json.loads(request_data.content)

        for teamworks_data in json_request_data:

            technicalteam_name = teamworks_data["cuadrilla"].upper()
            technicalteam_queryset = CuadrillaTecnicaModel.objects.filter(
                name=technicalteam_name
            )

            if not technicalteam_queryset.exists():
                raise serializers.ValidationError(
                    f'No record found for "{technicalteam_name}" in Technical Team.',
                    status.HTTP_400_BAD_REQUEST,
                )

            model, created = ConexionesCompletedWorkModel.objects.update_or_create(
                date=date_query_param,
                quantity=teamworks_data["cantidad"],
                technical_team_id=technicalteam_queryset.values().first()["id"],
            )

            if created:
                print(f"{model} created: {created}")

        return True

    def list(self, request, *args, **kwargs):
        return super().list(self, request, *args, **kwargs)

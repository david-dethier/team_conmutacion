from rest_framework import viewsets
from rest_framework.response import Response
from rest_framework.exceptions import APIException
from rest_framework.decorators import action
from api.v1.gis.models import CiudadModel
from api.v1.red.serializers import NodoSerializer
from api.v1.red.models import Nodo
from api.v1.red import services
from api.v1.red import selectors
from rest_framework import status
from typing import Optional


class NodoViewSet(viewsets.ModelViewSet):

    serializer_class = NodoSerializer
    queryset = Nodo.objects.select_related().all()

    @action(detail=False, methods=["get"])
    def importar_nodos(self, request):
        info = selectors.fetch_info_de_nodos()

        if info["status_code"] != status.HTTP_200_OK:
            raise APIException(info, info["status_code"])

        information = services.parse_data_info_de_nodo(info)
        serializer = self.get_serializer(data=information, many=True)

        if serializer.is_valid(raise_exception=True):
            nodos = []

            for item in serializer.validated_data:
                nodos.append(
                    Nodo(
                        id=len(nodos) + 1,
                        chasis=item["chasis"],
                        denominacion=item["denominacion"],
                        modems_online=item["modems_online"],
                        modems_offline=item["modems_offline"],
                        modems_percent_online=item["modems_percent_online"],
                        ciudad=item["ciudad"],
                    )
                )

            Nodo.objects.all().delete()
            Nodo.objects.bulk_create(nodos)

            headers = self.get_success_headers(serializer.data)
            return Response(
                serializer.data, status=status.HTTP_201_CREATED, headers=headers
            )

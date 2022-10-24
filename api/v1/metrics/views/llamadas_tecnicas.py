from rest_framework.decorators import action
from rest_framework import viewsets
from rest_framework.response import Response
from rest_framework import status
from api.v1.metrics.serializers.llamadas_tecnicas import CallModelSerializer
from api.v1.metrics.models.llamadas_tecnicas import LlamadasTecnicasModel
from api.v1.metrics.services import parse_llamadas_tecnicas


class LlamadaTecnicaViewSet(viewsets.ReadOnlyModelViewSet):

    serializer_class = CallModelSerializer
    queryset = LlamadasTecnicasModel.objects.all()
    filterset_fields = ("fecha", "telefono", "origen_src", "destino_dst")

    @action(detail=False, methods=["post"])
    def importar_llamadas(self, request):
        saved_data = parse_llamadas_tecnicas(request.data)
        status_code = (
            status.HTTP_201_CREATED
            if len(saved_data) != 0
            else status.HTTP_204_NO_CONTENT
        )
        return Response(saved_data, status=status_code)

from rest_framework import serializers
from api.v1.metrics.models.monitoreos import (
    CablemodemCountMonitoredModel,
    NodoEventoModel,
    NodoEventoEquipoAfectadoModel,
)


class CablemodemCountMonitoredSerializer(serializers.ModelSerializer):
    class Meta:
        model = CablemodemCountMonitoredModel
        fields = "__all__"


class EventoDeNodoSerializer(serializers.ModelSerializer):
    class Meta:
        model = NodoEventoModel
        depth = 1
        fields = (
            "eventid",
            "nodo",
            "inicio",
            "antiguedad",
            "fin",
            "duracion",
            "tipo",
            "estado",
            "equipos_afectados",
            "equipos_caidos",
            "porcentaje_online",
            "afectados",
        )


class EventoDeNodoEquiposAdectadosSerializer(serializers.ModelSerializer):
    class Meta:
        model = NodoEventoEquipoAfectadoModel
        depth = 1
        fields = "__all__"

from rest_framework import serializers
from api.v1.metrics.models.llamadas_tecnicas import LlamadasTecnicasModel


class CallModelSerializer(serializers.ModelSerializer):
    class Meta:
        model = LlamadasTecnicasModel
        fields = "__all__"

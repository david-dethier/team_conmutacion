from rest_framework import serializers
from api.v1.gis.serializers import CiudadSerializer
from api.v1.red.models import Nodo
from collections import OrderedDict

class NodoSerializer(serializers.ModelSerializer):
    class Meta:
        model = Nodo
        fields = "__all__"

    def to_representation(self, instance):
        representation = super().to_representation(instance)
        if type(instance) is Nodo:
            representation["ciudad"] = CiudadSerializer(instance.ciudad).data
        elif type(instance) is OrderedDict:
            representation["ciudad"] = CiudadSerializer(instance["ciudad"]).data
        return representation

from rest_framework import serializers
from .models import DomicilioGeoLocalizadoModel
from .models import CiudadModel


class CiudadSerializer(serializers.ModelSerializer):

    class Meta:
        model = CiudadModel
        fields = "__all__"


class DomicilioGeoLocalizadoSerializer(serializers.ModelSerializer):
    class Meta:
        model = DomicilioGeoLocalizadoModel
        fields = "__all__"

    def validate_calle(self, attrs):
        sanitize_calle:str = attrs.title()
        return super().validate(sanitize_calle)

from rest_framework import serializers
from api.v1.metrics.models.conexiones import ConexionesCompletedWorkModel


class CompletedWorkConnectionSerializer(serializers.ModelSerializer):
    class Meta:
        model = ConexionesCompletedWorkModel
        fields = "__all__"

    def to_representation(self, instance):
        return {
            "date": str(instance.date),
            "quantity": instance.quantity,
            "technical_team": instance.technical_team.alias,
        }

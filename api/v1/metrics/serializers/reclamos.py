from rest_framework import serializers
from api.v1.metrics.models.reclamos import ReclamosCompletedWorkModel


class CompletedWorkClaimsSerializer(serializers.ModelSerializer):
    class Meta:
        model = ReclamosCompletedWorkModel
        fields = "__all__"

    def to_representation(self, instance):
        return {
            "date": str(instance.date),
            "quantity": instance.quantity,
            "technical_team": instance.technical_team.alias,
        }

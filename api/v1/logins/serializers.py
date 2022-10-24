from rest_framework import serializers
from api.v1.logins.models import UserLoginModel


class LoginSerializer(serializers.ModelSerializer):
    class Meta:
        model = UserLoginModel
        fields = "__all__"

    def create(self, validated_data):
        return super().create(validated_data)

    def update(self, instance, validated_data):
        return super().update(instance, validated_data)

    def to_representation(self, instance):
        instance.created_on = instance.created_on.strftime("%Y-%m-%d %H:%M:%S")
        instance.modified_on = instance.modified_on.strftime("%Y-%m-%d %H:%M:%S")
        return super().to_representation(instance)


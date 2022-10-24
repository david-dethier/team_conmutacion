from rest_framework import viewsets
from api.v1.logins.serializers import LoginSerializer
from api.v1.logins.models import UserLoginModel


class LoginViewSet(viewsets.ModelViewSet):

    serializer_class = LoginSerializer
    queryset = UserLoginModel.objects.all()

    def list(self, request, *args, **kwargs):
        return super().list(request, *args, **kwargs)

    def create(self, request, *args, **kwargs):
        
        return super().create(request, *args, **kwargs)

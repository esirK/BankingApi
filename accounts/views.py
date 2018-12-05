from django.contrib.auth import get_user_model
from rest_framework import generics, status, mixins
from rest_framework.permissions import IsAdminUser
from rest_framework.response import Response

from accounts.serializers import (TellerSerializer,
                                  CustomerSerializer,
                                  LoginSerializer,
                                  UsersSerializer)
from transactions.permissions import IsAdminAndActivated

User = get_user_model()

class UserRegistrationAPIView(generics.CreateAPIView):
    queryset = User.objects.all()
    permission_classes = [IsAdminUser]

    def get_serializer_class(self, *args, **kwargs):
        if self.request.user.is_manager:
            return TellerSerializer
        if self.request.user.is_teller:
            return CustomerSerializer


class UserLoginAPIView(generics.CreateAPIView):
    queryset = User.objects.all()
    serializer_class = LoginSerializer

    def post(self, request, *args, **kwargs):
        data = request.data
        serializer = self.serializer_class(data=data)
        serializer.is_valid(raise_exception=True)

        return Response(serializer.validated_data, status=status.HTTP_200_OK)


class AllUsersAPIView(mixins.ListModelMixin, mixins.RetrieveModelMixin, generics.GenericAPIView):
    queryset = User.objects.all()
    serializer_class = UsersSerializer
    permission_classes = [IsAdminAndActivated]

    def get(self, request, *args, **kwargs):
        if kwargs.get('pk'):
            return self.retrieve(request, *args, **kwargs)
        else:
            return self.list(request, *args, **kwargs)

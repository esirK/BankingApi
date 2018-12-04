from django.contrib.auth import get_user_model
from rest_framework import generics
from rest_framework.permissions import IsAdminUser

from accounts.serializers import TellerSerializer, CustomerSerializer

User = get_user_model()

class UserRegistrationAPIView(generics.CreateAPIView):
    queryset = User.objects.all()
    permission_classes = [IsAdminUser]

    def get_serializer_class(self, *args, **kwargs):
        if self.request.user.is_manager:
            return TellerSerializer
        if self.request.user.is_teller:
            return CustomerSerializer


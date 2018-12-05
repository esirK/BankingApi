from rest_framework import generics

from transactions.permissions import IsAdminAndActivated, IsAuthenticatedAndActivated
from .serializers import TopUpSerializer, WithdrawSerializer
from .models import Transaction


class TopUpAPIView(generics.CreateAPIView):
    serializer_class = TopUpSerializer
    queryset = Transaction.objects.all()
    permission_classes = [IsAdminAndActivated]


class WithdrawAPIView(generics.CreateAPIView):
    serializer_class = WithdrawSerializer
    queryset = Transaction.objects.all()
    permission_classes = [IsAuthenticatedAndActivated]

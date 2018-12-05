from rest_framework import generics

from transactions.permissions import (IsAdminAndActivated,
                                      IsAuthenticatedAndActivated)
from .serializers import (TopUpSerializer,
                          WithdrawSerializer,
                          TransferSerializer)
from .models import Transaction


class TopUpAPIView(generics.CreateAPIView):
    serializer_class = TopUpSerializer
    queryset = Transaction.objects.all()
    permission_classes = [IsAdminAndActivated]


class WithdrawAPIView(generics.CreateAPIView):
    serializer_class = WithdrawSerializer
    queryset = Transaction.objects.all()
    permission_classes = [IsAuthenticatedAndActivated]


class TransferAPIView(generics.CreateAPIView):
    serializer_class = TransferSerializer
    queryset = Transaction.objects.all()
    permission_classes = [IsAuthenticatedAndActivated]

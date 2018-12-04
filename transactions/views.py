from rest_framework import generics

from transactions.permissions import IsAdminAndActivated
from .serializers import TransactionSerializer
from .models import Transaction

class TransactionsAPIView(generics.CreateAPIView):
    serializer_class = TransactionSerializer
    queryset = Transaction.objects.all()
    permission_classes = [IsAdminAndActivated]

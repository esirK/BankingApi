from rest_framework import generics

from transactions.permissions import IsAdminAndActivated
from .serializers import TopUpSerializer
from .models import Transaction

class TopUpAPIView(generics.CreateAPIView):
    serializer_class = TopUpSerializer
    queryset = Transaction.objects.all()
    permission_classes = [IsAdminAndActivated]

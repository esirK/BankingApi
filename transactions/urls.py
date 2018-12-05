from django.urls import path

from .views import (TopUpAPIView, WithdrawAPIView)


app_name = 'transactions'

urlpatterns = [
    path('topup/', TopUpAPIView.as_view(), name='topup'),
    path('withdraw/', WithdrawAPIView.as_view(), name='withdraw'),
]

from django.urls import path

from .views import (TopUpAPIView)


app_name = 'transactions'

urlpatterns = [
    path('topup/', TopUpAPIView.as_view(), name='topup'),
]

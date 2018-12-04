from django.urls import path

from .views import (TransactionsAPIView)


app_name = 'transactions'

urlpatterns = [
    path('transact/', TransactionsAPIView.as_view(), name='transact'),
]

from django.urls import path

from .views import UserRegistrationAPIView


app_name = 'accounts'

urlpatterns = [
    path('register/', UserRegistrationAPIView.as_view(), name='register'),
]

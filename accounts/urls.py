from django.urls import path

from .views import (UserRegistrationAPIView,
                    UserLoginAPIView)


app_name = 'accounts'

urlpatterns = [
    path('register/', UserRegistrationAPIView.as_view(), name='register'),
    path('login/', UserLoginAPIView.as_view(), name='login'),
]

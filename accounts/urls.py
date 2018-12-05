from django.urls import path

from .views import (UserRegistrationAPIView,
                    UserLoginAPIView,
                    AllUsersAPIView,
                    )


app_name = 'accounts'

urlpatterns = [
    path('register/', UserRegistrationAPIView.as_view(), name='register'),
    path('login/', UserLoginAPIView.as_view(), name='login'),
    path('users/', AllUsersAPIView.as_view(), name='users'),
    path('users/<int:pk>', AllUsersAPIView.as_view(), name='users'),
]

from django.contrib.auth.models import AbstractUser, BaseUserManager
from django.db import models


class User(AbstractUser):
    email = models.EmailField(max_length=50, unique=True)

    is_active = models.BooleanField(
        'active',
        default=False,
        help_text= (
            'All Users are inactive by default.'
            'This should be set to True when a User login for the first time and change their default password.'
        )
    )

    is_manager = models.BooleanField(
        'manager',
        default=False,
        help_text=(
            'Managers have special permissions and thus cannot be created via the API.'
        )
    )
    is_teller = models.BooleanField(
        'teller',
        default=False,
        help_text=(
            'Tellers have permissions for creating customers'
        )
    )
    is_customer = models.BooleanField(
        'customer',
        default=False,
        help_text=(
            'Customers can have accounts with the bank.'
        )
    )
    REQUIRED_FIELDS = ['email']

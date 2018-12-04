import jwt
from django.conf import settings
from django.contrib.auth.models import AbstractUser, BaseUserManager
from django.db import models


class CustomManager(BaseUserManager):
    use_in_migrations = True

    def _create_user(self, **fields):
        email = fields.pop('email')
        password = fields.get('password')

        if not email:
            raise ValueError("Email address is required")

        email = self.normalize_email(email)
        user = self.model(email=email, **fields)
        user.set_password(password)
        user.save(using=self._db)
        return user

    def create_superuser(self, **fields):
        fields.setdefault('is_staff', True)
        fields.setdefault('is_superuser', True)
        fields.setdefault('is_active', True)

        self._create_user(**fields)

    def create_user(self, **fields):
        fields.setdefault('is_staff', False)
        fields.setdefault('is_superuser', False)

        return self._create_user(**fields)

    def create_manager(self, **fields):
        fields.setdefault('is_manager', True)
        fields.setdefault('is_staff', True)

        return self._create_user(**fields)

    def create_teller(self, **fields):
        fields.setdefault('is_teller', True)
        fields.setdefault('is_staff', True)

        return self._create_user(**fields)

    def create_customer(self, **fields):
        fields.setdefault('is_customer', True)

        return self._create_user(**fields)


class User(AbstractUser):
    objects = CustomManager()
    email = models.EmailField(max_length=50, unique=True)

    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = ['username']

    is_activated = models.BooleanField(
        'is_activated',
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

    @property
    def token(self):
        """
        Generates the token and allows the token
        to be called by `user.token`
        :return string
        """
        token = jwt.encode(
            {
                "id": self.id,
                "username": self.username,
                "email": self.email,
            },
            settings.SECRET_KEY, algorithm='HS256').decode()
        return token

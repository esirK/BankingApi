from django.test import TestCase

from django.contrib.auth import get_user_model
from rest_framework.reverse import reverse
from rest_framework.test import APIClient

User = get_user_model()
client = APIClient()


class BaseTestCase(TestCase):
    @classmethod
    def setUpClass(cls):
        super().setUpClass()
        cls.manager = User.objects.create_manager(
            username="Manager",
            email="johndoe@manager.com",
            password="Manager199407#"
        )
        cls.teller1 = User.objects.create_teller(
            username="Teller1",
            email="teller1@teller.com",
            password="Teller19407#"
        )
        cls.customer1 = User.objects.create_customer(
            username="Customer1",
            email="customer1@customer.com",
            password="Customer19407#"
        )
        cls.data = {
            "username": "Teller2",
            "email": "teller2@teller.com",
            "password": "Teller19407#",
            "confirm_password": "Teller19407#"
        }

        #URLS
        cls.login_url = reverse('accounts:login')
        cls.registration_url = reverse('accounts:register')
        cls.users_url = reverse('accounts:users')


    @classmethod
    def tearDownClass(cls):
        super().tearDownClass()

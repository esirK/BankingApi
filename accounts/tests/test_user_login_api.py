from django.test import TestCase

from django.contrib.auth import get_user_model
from rest_framework.reverse import reverse
from rest_framework.test import APIClient

User = get_user_model()
client = APIClient()


class TestUserLoginApi(TestCase):
    def setUp(self):
        self.login_url = reverse('accounts:login')

        self.manager = User.objects.create_manager(
            username="Manager",
            email="johndoe@manager.com",
            password="Manager199407#"
        )
        self.teller1 = User.objects.create_teller(
            username="Teller1",
            email="teller1@teller.com",
            password="Teller19407#"
        )
        self.customer1 = User.objects.create_customer(
            username="Customer1",
            email="customer1@customer.com",
            password="Customer19407#"
        )

    def test_successful_login_returns_token(self):
        data = {
            'email': self.manager.email,
            'password': 'Manager199407#'
        }
        response = client.post(self.login_url, data=data)

        self.assertIn('token', response.json())
        self.assertEqual(200, response.status_code)

    def test_login_fails_for_invalid_credentials(self):
        data = {
            'email': self.manager.email,
            'password': 'WrongPassword'
        }
        response = client.post(self.login_url, data=data)

        self.assertIn('error', response.json())
        self.assertEqual(400, response.status_code)

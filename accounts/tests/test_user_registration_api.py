from django.test import TestCase

from rest_framework.reverse import reverse
from django.contrib.auth import get_user_model
from rest_framework.test import APIClient

User = get_user_model()
client = APIClient()


class TestUserRegistrationAPI(TestCase):
    def setUp(self):
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

        self.data = {
            "username": "Teller2",
            "email": "teller2@teller.com",
            "password": "Teller19407#",
            "confirm_password": "Teller19407#"
        }

        self.registration_url = reverse('accounts:register')


    def test_only_staff_users_can_register_new_users(self):

        response = client.post('{}'.format(self.registration_url,
                                            data=self.data))
        self.assertEqual(403, response.status_code)

    def test_customer_cannot_register_a_new_user(self):
        response = client.post(self.registration_url,
                                           HTTP_AUTHORIZATION="Token {}".format(self.customer1.token),
                                           data=self.data)
        self.assertEqual(response.data, {
            'detail': 'You do not have permission to perform this action.'
        })
        self.assertEqual(403, response.status_code)

    def test_tellers_can_create_new_customers(self):
        data = self.data
        data['username'] = "Customer2"
        data['email'] = "customer2@customer.com"

        count = User.objects.count()

        response = client.post(self.registration_url,
                               HTTP_AUTHORIZATION="Token {}".format(self.teller1.token),
                               data=data)

        self.assertEqual(count+1, User.objects.count())
        self.assertTrue(User.objects.last().is_customer)
        self.assertEqual(201, response.status_code)


    def testManagers_can_create_new_tellers(self):
        data = self.data
        data['username'] = "Teller3"
        data['email'] = "teller3@teller.com"

        count = User.objects.count()

        response = client.post(self.registration_url,
                               HTTP_AUTHORIZATION="Token {}".format(self.manager.token),
                               data=data)
        self.assertEqual(count + 1, User.objects.count())
        self.assertTrue(User.objects.last().is_teller)
        self.assertEqual(201, response.status_code)

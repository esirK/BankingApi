from django.contrib.auth import get_user_model

from accounts.models import CustomerBankAccount
from accounts.tests import BaseTestCase

User = get_user_model()


class TestUserRegistrationAPI(BaseTestCase):
    def test_only_staff_users_can_register_new_users(self):

        response = self.client.post('{}'.format(self.registration_url,
                                            data=self.data))
        self.assertEqual(403, response.status_code)

    def test_customer_cannot_register_a_new_user(self):
        response = self.client.post(self.registration_url,
                                           HTTP_AUTHORIZATION="Token {}".format(self.customer1.token),
                                           data=self.data)
        self.assertEqual(response.data, {
            'detail': 'You do not have permission to perform this action.'
        })
        self.assertEqual(403, response.status_code)

    def test_tellers_can_create_new_customers(self):
        data = dict(self.data)
        data['username'] = "Customer2"
        data['email'] = "customer2@customer.com"

        count = User.objects.count()

        response = self.client.post(self.registration_url,
                               HTTP_AUTHORIZATION="Token {}".format(self.teller1.token),
                               data=data)

        self.assertEqual(count+1, User.objects.count())
        self.assertTrue(User.objects.last().is_customer)
        self.assertEqual(201, response.status_code)

    def test_managers_can_create_new_tellers(self):
        data = dict(self.data)
        data['username'] = "Teller3"
        data['email'] = "teller3@teller.com"

        count = User.objects.count()

        response = self.client.post(self.registration_url,
                               HTTP_AUTHORIZATION="Token {}".format(self.manager.token),
                               data=data)
        self.assertEqual(count + 1, User.objects.count())
        self.assertTrue(User.objects.last().is_teller)
        self.assertEqual(201, response.status_code)

    def test_bank_accounts_are_created_once_a_customer_is_registered(self):
        data = dict(self.data)
        data['username'] = "Customer3"
        data['email'] = "customer3@customer.com"

        count = CustomerBankAccount.objects.count()
        self.client.post(self.registration_url,
                               HTTP_AUTHORIZATION="Token {}".format(self.teller1.token),
                               data=data)

        self.assertEqual(count + 1, CustomerBankAccount.objects.count())

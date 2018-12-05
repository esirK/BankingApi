from django.contrib.auth import get_user_model
from rest_framework import status

from accounts.models import CustomerBankAccount

User = get_user_model()

from . import BaseTestCase

class TestTopUpTransaction(BaseTestCase):
    def test_non_logged_in_user_cannot_perform_a_transaction(self):
        response = self.client.post(self.top_up_url, data=self.data)
        self.assertEqual(response.data, {
            'detail': 'Authentication credentials were not provided.'
        })
        self.assertEqual(status.HTTP_403_FORBIDDEN, response.status_code)

    def test_un_activated_authenticated_staff_users_cannot_perform_a_transaction(self):
        response = self.client.post(self.top_up_url,
                               data=self.data,
                               HTTP_AUTHORIZATION="Token {}".format(self.teller.token))

        self.assertEqual(response.data, {
            'detail': 'You do not have permission to perform this action.'
        })
        self.assertEqual(status.HTTP_403_FORBIDDEN, response.status_code)

    def test_customers_cannot_access_the_top_up_endpoint(self):
        """
        Tests to ensure that normal customer cannot top_up their accounts.
        This would be a bug if it was to happen.
        """
        customer = User.objects.create_customer(
            username="Customer1",
            email="customer1@customer.com",
            password="Customer19407#"
        )
        customer.is_activated = True
        customer.save()

        token = customer.token
        response = self.client.post(self.top_up_url,
                               data=self.data,
                               HTTP_AUTHORIZATION="Token {}".format(token))
        self.assertEqual(response.data, {
            'detail': 'You do not have permission to perform this action.'
        })
        self.assertEqual(status.HTTP_403_FORBIDDEN, response.status_code)

    def test_authenticated_staff_can_top_up_a_customer_account(self):
        teller = User.objects.create_teller(
            username="Teller1",
            email="teller1@teller.com",
            password="Teller9407#"
        )
        teller.is_activated = True
        teller.save()

        response = self.client.post(self.top_up_url,
                               data=self.data,
                               HTTP_AUTHORIZATION="Token {}".format(teller.token))
        account_balance = CustomerBankAccount.objects.get(owner=self.customer).balance

        self.assertEqual(account_balance, self.customer_account.balance + int(self.data.get('amount')))
        self.assertEqual(status.HTTP_201_CREATED, response.status_code)

from rest_framework import status

from accounts.models import CustomerBankAccount
from transactions.tests import BaseTestCase

from django.contrib.auth import get_user_model

User = get_user_model()

class WithdrawTransaction(BaseTestCase):
    def test_non_logged_in_user_cannot_perform_a_withdraw(self):
        response = self.client.post(self.withdraw_url, data=self.data)
        self.assertEqual(response.data, {
            'detail': 'Authentication credentials were not provided.'
        })
        self.assertEqual(status.HTTP_403_FORBIDDEN, response.status_code)

    def test_logged_in_users_can_perform_a_withdraw(self):
        self.teller.is_activated = True
        self.teller.save()

        response = self.client.post(self.withdraw_url,
                                    data=self.data,
                                    HTTP_AUTHORIZATION="Token {}".format(self.teller.token))

        customer_balance = CustomerBankAccount.objects.get(id=self.data.get('performed_on')).balance

        self.assertEqual(customer_balance, self.customer_account.balance - self.data.get('amount'))
        self.assertEqual(status.HTTP_201_CREATED, response.status_code)

    def test_a_customer_can_perform_a_withdraw_on_their_account(self):
        self.customer.is_activated = True
        self.customer.save()
        response = self.client.post(self.withdraw_url,
                                    data=self.data,
                                    HTTP_AUTHORIZATION="Token {}".format(self.customer.token))

        customer_balance = CustomerBankAccount.objects.get(id=self.data.get('performed_on')).balance

        self.assertEqual(customer_balance, self.customer_account.balance - self.data.get('amount'))
        self.assertEqual(status.HTTP_201_CREATED, response.status_code)

    def test_a_customer_cannot_perform_a_withdraw_for_another_customer(self):
        customer = User.objects.create_customer(
            username="Customer1",
            email="customer1@customer.com",
            password="Customer19407#"
        )
        customer.is_activated = True
        customer.save()

        response = self.client.post(self.withdraw_url,
                                    data=self.data,
                                    HTTP_AUTHORIZATION="Token {}".format(customer.token))

        self.assertEqual(status.HTTP_400_BAD_REQUEST, response.status_code)

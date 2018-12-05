from rest_framework import status

from accounts.models import CustomerBankAccount
from transactions.tests import BaseTestCase

from django.contrib.auth import get_user_model

User = get_user_model()


class TransferTransactionTestCase(BaseTestCase):
    def test_non_logged_in_user_cannot_perform_a_transaction(self):
        response = self.client.post(self.transfer_url, data=self.data)
        self.assertEqual(response.data, {
            'detail': 'Authentication credentials were not provided.'
        })
        self.assertEqual(status.HTTP_403_FORBIDDEN, response.status_code)

    def test_logged_in_users_can_perform_a_transfer(self):
        self.teller.is_activated = True
        self.teller.save()

        customer1 = User.objects.create_customer(
            username="Customer1",
            email="customer1@customer.com",
            password="Customer19407#"
        )
        customer1_account = CustomerBankAccount.objects.create(owner=customer1, balance=1000)

        data = dict(self.data)
        data['transfer_to'] = customer1_account.id

        response = self.client.post(self.transfer_url,
                                    data=data,
                                    HTTP_AUTHORIZATION="Token {}".format(self.teller.token))

        sender_balance = CustomerBankAccount.objects.get(id=self.data.get('performed_on')).balance
        receiver_balance = CustomerBankAccount.objects.get(id=data.get('transfer_to')).balance

        self.assertEqual(sender_balance, self.customer_account.balance - self.data.get('amount'))
        self.assertEqual(receiver_balance, customer1_account.balance + self.data.get('amount'))
        self.assertEqual(status.HTTP_201_CREATED, response.status_code)

    def test_a_user_can_not_transfer_funds_to_the_same_account(self):
        self.teller.is_activated = True
        self.teller.save()

        data = dict(self.data)
        data['transfer_to'] = data.get('performed_on')

        response = self.client.post(self.transfer_url,
                                    data=data,
                                    HTTP_AUTHORIZATION="Token {}".format(self.teller.token))
        self.assertEqual(status.HTTP_400_BAD_REQUEST, response.status_code)

    def test_a_user_can_not_transfer_funds_if_they_do_not_have_enough_funds(self):
        self.teller.is_activated = True
        self.teller.save()

        customer = User.objects.create_customer(
            username="Customer0",
            email="customer0@customer.com",
            password="Customer19407#"
        )
        customer1_account = CustomerBankAccount.objects.create(owner=customer, balance=0)
        customer1 = User.objects.create_customer(
            username="Customer5",
            email="customer5@customer.com",
            password="Customer19407#"
        )
        customer_account = CustomerBankAccount.objects.create(owner=customer1, balance=1000)

        data = dict(self.data)
        data['transfer_to'] = customer_account.id
        data['performed_on'] = customer1_account.id

        response = self.client.post(self.transfer_url,
                                    data=data,
                                    HTTP_AUTHORIZATION="Token {}".format(self.teller.token))
        self.assertEqual(response.json(), ['You do not have enough balance to perform this action.'])
        self.assertEqual(status.HTTP_400_BAD_REQUEST, response.status_code)

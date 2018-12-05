from django.contrib.auth import get_user_model
from django.test import TestCase
from rest_framework.reverse import reverse
from rest_framework.test import APIClient

from accounts.models import CustomerBankAccount

User = get_user_model()
client = APIClient()


class BaseTestCase(TestCase):
    @classmethod
    def setUpClass(cls):
        super().setUpClass()
        cls.teller = User.objects.create_teller(
            username="Teller",
            email="teller@teller.com",
            password="Teller9407#"
        )
        cls.customer = User.objects.create_customer(
            username="Customer",
            email="customer@customer.com",
            password="Customer19407#"
        )
        cls.customer_account = CustomerBankAccount.objects.create(owner=cls.customer, balance=1000)

        cls.data = {
                "amount": 1000,
                "performed_on": cls.customer_account.id
        }
        cls.client = APIClient()

        #URLS
        cls.top_up_url = reverse('transactions:topup')
        cls.withdraw_url = reverse('transactions:withdraw')

    @classmethod
    def tearDownClass(cls):
        super().tearDownClass()

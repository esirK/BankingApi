from django.test import TestCase

from accounts.models import User

class TestUserModel(TestCase):
    def setUp(self):
        self.default_user = User.objects.create_user(
            email='esirkings@gmail.com',
            username='esir',
            password='199407'
        )

    def test_users_are_inactive_on_creation(self):
        self.assertFalse(self.default_user.is_active)

    def test_create_manager_command(self):
        manager = User.objects.create_manager(
            email='esirkings@admin.com',
            username='Admin',
            password='Admin199407'
        )
        self.assertEqual(2, User.objects.count())
        self.assertTrue(manager.is_manager)
        self.assertTrue(manager.is_staff)
        self.assertFalse(manager.is_teller)
        self.assertFalse(manager.is_customer)


    def test_create_teller_command(self):
        teller = User.objects.create_teller(
            email='esirkings@teller.com',
            username='Teller',
            password='Teller199407'
        )
        self.assertEqual(2, User.objects.count())
        self.assertTrue(teller.is_teller)
        self.assertTrue(teller.is_staff)
        self.assertFalse(teller.is_manager)
        self.assertFalse(teller.is_customer)


    def test_create_customer_command(self):
        customer = User.objects.create_customer(
            email='esirkings@customer.com',
            username='Customer',
            password='Customer199407'
        )
        self.assertEqual(2, User.objects.count())
        self.assertTrue(customer.is_customer)
        self.assertFalse(customer.is_staff)
        self.assertFalse(customer.is_manager)
        self.assertFalse(customer.is_teller)

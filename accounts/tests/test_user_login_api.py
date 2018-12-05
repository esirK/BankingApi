from django.contrib.auth import get_user_model

from accounts.tests import BaseTestCase

User = get_user_model()

class TestUserLoginApi(BaseTestCase):
    def test_successful_login_returns_token(self):
        data = {
            'email': self.manager.email,
            'password': 'Manager199407#'
        }
        response = self.client.post(self.login_url, data=data)

        self.assertIn('token', response.json())
        self.assertEqual(200, response.status_code)

    def test_login_fails_for_invalid_credentials(self):
        data = {
            'email': self.manager.email,
            'password': 'WrongPassword'
        }
        response = self.client.post(self.login_url, data=data)

        self.assertIn('error', response.json())
        self.assertEqual(400, response.status_code)

from rest_framework import status

from accounts.tests import BaseTestCase


class TestAllUsersApi(BaseTestCase):
    def test_activated_authenticated_staff_can_view_all_users(self):
        response = self.client.get(self.users_url,
                                    HTTP_AUTHORIZATION="Token {}".format(self.teller1.token),
                                    data=self.data)
        self.assertEqual(status.HTTP_403_FORBIDDEN, response.status_code)

        self.teller1.is_activated = True
        self.teller1.save()

        response = self.client.get(self.users_url,
                                    HTTP_AUTHORIZATION="Token {}".format(self.teller1.token),
                                    data=self.data)
        self.assertEqual(status.HTTP_200_OK, response.status_code)

    def test_non_staff_can_not_view_all_users(self):
        self.customer1.is_activated = True
        self.customer1.save()

        response = self.client.get(self.users_url,
                                   HTTP_AUTHORIZATION="Token {}".format(self.customer1.token),
                                   data=self.data)
        self.assertEqual(status.HTTP_403_FORBIDDEN, response.status_code)

    def test_authenticated_user_can_view_single_user(self):
        self.manager.is_activated = True
        self.manager.save()
        response = self.client.get(self.users_url+"{}".format(self.customer1.id,),
                                   HTTP_AUTHORIZATION="Token {}".format(self.manager.token),
                                   data=self.data)
        self.assertEqual(response.json().get('pk'), self.customer1.id)
        self.assertEqual(status.HTTP_200_OK, response.status_code)

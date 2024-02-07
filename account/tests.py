from django.test import TestCase
from django.test.client import Client

from test_utils.account_utils import create_test_user
from .models import Account


#                    Tests
# -------------------------------------------------
# -------------------------------------------------


class LoginAPITest(TestCase):
    """
    Test the login api endpoint view
    """

    def setUp(self) -> None:
        create_test_user()
        self.api_client = Client()
        self.endpoint = "http://127.0.0.1:8000/accounts/login"
        self.request_data = {
            "username": "test_username",
            "password": "test_password"
        }

    def check_invalid_credentials(self, res, credential_type):
        no_of_accounts = len(Account.objects.all())
        self.assertEqual(res.status_code, 404,
                         f"Status code 404 must be returned for invalid {credential_type} credentials")
        self.assertNotIn("token", res.json(), f"No token should be returned for invalid {credential_type} credentials")
        self.assertEqual(no_of_accounts, no_of_accounts,
                         f"No user account must be created when passed an invalid {credential_type}")

    def test_valid_credentials(self):
        """
        Tests if token is returned for valid credentials
        """
        res = self.api_client.post(self.endpoint, data=self.request_data)
        self.assertEqual(res.status_code, 200,
                         f"Login endpoint must return a status code 200 when valid credentials are provided not {res.status_code}")
        self.assertIn("token", res.json(),
                      "Authentication Token should be included in the response to valid credentials")

    def test_invalid_username_credentials(self):
        """
        Test if appropriate message is displayed for invalid username credential
        """

        self.request_data["username"] = "invalid_username"
        res = self.api_client.post(self.endpoint, data=self.request_data)
        self.check_invalid_credentials(res, "username")
        self.assertEqual(res.json()['message'].lower(), "invalid username")

    def test_invalid_password_credentials(self):
        """
        Test if appropriate message is displayed for invalid password credential
        """
        self.request_data["password"] = "invalid_username"
        res = self.api_client.post(self.endpoint, data=self.request_data)
        self.check_invalid_credentials(res, "password")
        self.assertEqual(res.json()['message'].lower(), "invalid password")

    def test_no_param_was_given(self):
        """
        Test if response is treated accordingly if empty data or incomplete data is passed
        """
        res = self.api_client.post(self.endpoint, data={})
        self.check_invalid_credentials(res, "empty param")

from django.contrib.auth.hashers import check_password
from rest_framework.authtoken.models import Token
from rest_framework.test import APITestCase

from test_utils.account_utils import create_test_user
from .models import Account



#               Base Data Base setup
#  ______________________________________________
# _______________________________________________


class BaseTestSetupData(APITestCase):

    def setUp(self) -> None:
        self.user = create_test_user()
        self.token, created = Token.objects.get_or_create(user=self.user)
        self.headers = {
            "Authorization": f"Token {self.token.key}",
            "Content-Type": "application/json"
        }
        self.endpoint = "/accounts/forgot/username"




#                    Tests
# -------------------------------------------------
# -------------------------------------------------



class LoginDataAPITest(BaseTestSetupData):
    """
    Test the login api endpoint view
    """

    def setUp(self) -> None:
        self.request_data = {
            "username": "test_username",
            "password": "test_password"
        }
        super().setUp()
        self.endpoint = "/accounts/login"


    def check_invalid_credentials(self, res, credential_type):
        no_of_accounts = len(Account.objects.all())
        self.assertEqual(res.status_code, 404,
                         f"Status code 404 must be returned for invalid {credential_type} credentials")
        self.assertNotIn("token", res.json(), f"No token should be returned for invalid {credential_type} credentials")
        self.assertEqual(no_of_accounts, no_of_accounts,
                         f"No user account must be created when passed an invalid {credential_type}")

    def test_valid_credentials_with_username(self):
        """
        Tests if token is returned for valid credentials using username
        """
        res = self.client.post(self.endpoint, data=self.request_data)
        self.assertEqual(res.status_code, 200,
                         f"Login endpoint must return a status code 200 when valid credentials are provided not {res.status_code}")
        self.assertIn("token", res.json(),
                      "Authentication Token should be included in the response to valid credentials")

    def test_valid_credentials_with_email(self):
        """
        Tests if token is returned for valid credentials using username
        """
        email_credential = self.request_data.copy()
        email_credential['username'] = "testemail@email.com"
        res = self.client.post(self.endpoint, data=email_credential)
        self.assertEqual(res.status_code, 200,
                         f"Login endpoint must return a status code 200 when valid credentials are provided not {res.status_code}")
        self.assertIn("token", res.json(),
                      "Authentication Token should be included in the response to valid credentials")

    def test_invalid_username_credentials(self):
        """
        Test if appropriate message is displayed for invalid username credential
        """

        self.request_data["username"] = "invalid_username"
        res = self.client.post(self.endpoint, data=self.request_data)
        self.check_invalid_credentials(res, "username")
        self.assertEqual(res.json()['responseMessage'].lower(), "invalid username / email")


    def test_invalid_password_credentials(self):
        """
        Test if appropriate message is displayed for invalid password credential
        """
        self.request_data["password"] = "invalid_username"
        res = self.client.post(self.endpoint, data=self.request_data)
        self.check_invalid_credentials(res, "password")
        self.assertEqual(res.json()['responseMessage'].lower(), "invalid password")

    def test_no_param_was_given(self):
        """
        Test if response is treated accordingly if empty data or incomplete data is passed
        """
        res = self.client.post(self.endpoint, data={})
        self.check_invalid_credentials(res, "empty param")
        

class ForgottenUsernameViewTestData(BaseTestSetupData):

    def test_valid_authentication_will_sends_a_message(self):
        """
        Tests if valid authentication token will return a successful response and if the email is sent to the user
        """
        print(self.endpoint)
        res = self.client.post(self.endpoint, headers=self.headers)
        self.assertEqual(res.status_code, 200)
        print(res.json())


class ChangePasswordViewTestData(BaseTestSetupData):
    """
    Tests the password change view
    """

    def setUp(self) -> None:
        super().setUp()
        self.endpoint = "/accounts/change/password"

    def test_incorrect_password_and_password_was_not_changed(self):
        """
        Test for an incorrect password requests
        """
        data = {
            "old_password": "falsePassword",
            "new_password": "falsePassword"
        }
        res = self.client.post(self.endpoint, headers=self.headers, data=data, format="json")
        self.assertEqual(res.status_code, 401)
        self.assertEqual(res.json()['responseMessage'], "incorrect password")
        user = Account.objects.get(id=self.user.id)

        if check_password(user.password, "newPassword"):
            raise AssertionError("User password should not change when an given an incorrect password")

    def test_correct_password_and_password_got_changed(self):
        data = {
            "old_password": "test_password",
            "new_password": "newPassword"
        }
        res = self.client.post(self.endpoint, headers=self.headers, data=data, format="json")
        self.assertEqual(res.status_code, 200)
        # Check if the user password has been changed
        user = Account.objects.get(id=self.user.id)
        if not check_password("newPassword", user.password):
            raise AssertionError("User password was not changed")

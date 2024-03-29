from django.core.exceptions import ObjectDoesNotExist
from rest_framework.authtoken.models import Token
from rest_framework.test import APITestCase

from account.models import Account
from farm_directory.models import FarmDirectory
from test_utils.account_utils import create_test_user, create_farm_directory_entry

BASE_TEST_ENDPOINT = "/"


class FarmDirectoryRegistrationTest(APITestCase):
    """
        TestCase for the registration View API
    """

    @classmethod
    def setUpClass(cls):
        # Create a one off setup data
        super(FarmDirectoryRegistrationTest, cls).setUpClass()
        cls.request_data = {
            "account": {
                "first_name": "test_first_name",
                "last_name": "test_last_name",
                "phone": 81249939392,
                "password": "11111111",
                "email": "weberdeveloper478@gmail.com",
            },
            "gender": "male",
            "street_address": "test street",
            "state": "test state",
            "country": "test country",
        }
        cls.endpoint = "/db/accounts/register"

    def check_used_credentials_responses(self, res, credential_type):
        self.assertEqual(res.status_code, 403, "Used credential must return a 403  forbidden error")
        self.assertIn(credential_type, res.json()['responseMessage']['errors'],
                      f"Must display an error message for field {credential_type} if the sent value has been used")

    def verify_account_is_not_created(self):

        # Get the number of available farm directory profiles
        no_of_farm_profiles_before = len(FarmDirectory.objects.all())
        # Get the number of available user accounts
        no_of_accounts_before = len(Account.objects.all())

        # Get the number of available farm directory profiles
        no_of_farm_profiles_after = len(FarmDirectory.objects.all())
        # Get the number of available user accounts
        no_of_accounts_after = len(Account.objects.all())

        self.assertEqual(no_of_accounts_after, no_of_accounts_before, "A new user account must not be created")
        self.assertEqual(no_of_farm_profiles_after, no_of_farm_profiles_before,
                         "A new farm directory profile must not be created")

    def test_valid_credentials(self):
        """
        Tests if username is created for valid credentials and its valid credentials creates a new user and farm
        directory entry
        """
        # Get the number of available farm directory profiles
        no_of_farm_profiles_before = len(FarmDirectory.objects.all())
        # Get the number of available user accounts
        no_of_accounts_before = len(Account.objects.all())

        res = self.client.post(self.endpoint, data=self.request_data, format="json")

        # Get the number of available farm directory profiles
        no_of_farm_profiles_after = len(FarmDirectory.objects.all())
        # Get the number of available user accounts
        no_of_accounts_after = len(Account.objects.all())

        self.assertEqual(res.status_code, 200, "Status code for valid credentials must be 200")
        self.assertEqual(no_of_accounts_after, (no_of_accounts_before + 1), "A new user account must be created")
        self.assertEqual(no_of_farm_profiles_after, (no_of_farm_profiles_before + 1),
                         "A new farm directory profile must be created")

        # Check if the view returns a username for the user
        self.assertIn("username", res.json()["responseBody"]['login'],
                      "Registration view must return a generated username for the registered user")
        try:
            account_exists = Account.objects.get(email=self.request_data["account"]['email'])
            try:
                FarmDirectory.objects.get(account=account_exists)
            except ObjectDoesNotExist:
                raise AssertionError("Farm profile for newly created account does not exist in the farm directory db")
        except ObjectDoesNotExist:
            raise AssertionError("Requested user account was added to the user database")

    def test_used_email(self):
        """
        Tests if response contains errors for the email field when a used email is sent
        Also tests if an account is not created for the entry
        """
        create_test_user(email="used_email@email.com")
        self.request_data['account']['email'] = "used_email@email.com"
        res = self.client.post(self.endpoint, data=self.request_data, format="json")
        self.assertEqual(res.status_code, 400, "Used credential must return a 403  forbidden error")
        self.assertIn("email", res.json()['responseBody']['errors']['account'],
                      "Must display an error message for field email if the sent value has been used")
        try:
            Account.objects.get(phone=self.request_data['account']['phone'])
            raise AssertionError("No account should be created for a used email address")
        except ObjectDoesNotExist:
            pass


class SearchDirectoryTest(APITestCase):
    """
    Tests the search directory endpoint. Usage of keyword search
    """

    @classmethod
    def setUpClass(cls) -> None:
        super(SearchDirectoryTest, cls).setUpClass()
        # Create 10 test users

        user = create_test_user(
            username=f"test1", email=f"test1@email.com", password=f"test1", phone="10202",
            first_name="Testing", last_name="Name"
        )

        # Create a farm directory for each created user
        # for user in test_users:
        entry = create_farm_directory_entry(
            user, gender="male", state="ogun", country="Nigeria", crop_type="maize")

        cls.endpoint = "/db/search/"
        cls.user = entry

    def check_keyword_search_response(self, res, expected_keyword):
        res_body = res.json()['responseBody']
        self.assertIn("keyword", res_body, "The parsed keyword should be included in the response")
        self.assertEqual(res_body['keyword'], expected_keyword,
                         "Server should be able to appropriately parse the search keyword")
        self.assertIn("results", res.json()["responseBody"], "Response should contains result for valid keyword search")

    def test_search_by_phone_keyword(self):
        """
        Test the output when queried with a number
        """

        res = self.client.get(self.endpoint + self.user.account.phone)
        self.assertEqual(res.status_code, 200)
        self.check_keyword_search_response(res, "phone")

    def test_search_by_crop_type(self):
        """
        Tests for the response when queried with a crop name prefix
        """
        res = self.client.get(self.endpoint + self.user.crop_type)
        self.assertEqual(res.status_code, 200)
        self.check_keyword_search_response(res, "crop_type")

    def test_search_by_state_name(self):
        """
        Test for the response when queried with a state name prefix
        """
        res = self.client.get(self.endpoint + self.user.state)
        self.assertEqual(res.status_code, 200)
        self.check_keyword_search_response(res, "state")

    def test_search_by_account_name(self):
        """
        Test for the response when queried with a state name prefix
        """
        res = self.client.get(self.endpoint + self.user.account.first_name)
        self.assertEqual(res.status_code, 200)
        self.check_keyword_search_response(res, "name")

    def test_no_match(self):
        res = self.client.get(self.endpoint + "lag")
        self.assertEqual(res.status_code, 404,
                         "Server should return a status code of 404 for un-matched search keywords")
        self.assertEqual(res.json()['responseBody'].lower(), "no match")


class UserProfileViewTest(APITestCase):
    """
     TestCase for getting user profile endpoint
    """

    @classmethod
    def setUpClass(cls):
        super(UserProfileViewTest, cls).setUpClass()
        cls.endpoint = "/db/users/farm/profile/get"
        user = create_test_user()
        create_farm_directory_entry(account=user)
        token, created = Token.objects.get_or_create(user=user)
        cls.headers = {
            "Authorization": f"Token {token.key}",
            "Content-Type": "application/json"
        }
        cls.user = user

    def test_valid_token_returns_user_credentials(self):
        res = self.client.post(self.endpoint, headers=self.headers)
        json_res = res.json()
        self.assertEqual(res.status_code, 200)
        self.assertEqual(json_res['success'], True)
        self.assertEqual(self.user.email, json_res['responseBody']['profile']['email'],
                         "The returned user email must match the token user")

    def test_no_token_sent(self):
        res = self.client.post(self.endpoint, headers={})
        self.assertEqual(res.status_code, 401, "Request without token must fail with a status code of 403")

    def test_invalid_token_fails(self):
        invalid_header = self.headers.copy()
        invalid_header["Authorization"] = "Token invalid_token"

        res = self.client.post(self.endpoint, headers=invalid_header)
        self.assertEqual(res.status_code, 401, "Invalid headers must fail with a status code of 404")


class FarmProfileUpdateTest(APITestCase):

    def setUp(self):
        self.endpoint = "/db/users/farm/profile/update"
        user = create_test_user()
        self.farm_entry = create_farm_directory_entry(account=user, crop_type="pawpaw")
        token, created = Token.objects.get_or_create(user=user)
        self.headers = {
            "Authorization": f"Token {token.key}",
            "Content-Type": "application/json"
        }
        self.user = user

    def test_user_data_are_updated_with_valid_token(self):
        """
        Test if the user account or Farm directory data are changed after an update request is sent
        """
        edit_data = {
            "first_name": "Bola",
            "gender": "female",
            "crop_type": "orange",
        }
        res = self.client.post(self.endpoint, data=edit_data, headers=self.headers, format="json")
        # Get the user table after update request has been sent
        user = Account.objects.get_by_natural_key(self.user.username)
        # Get the farm directory user record after the update request has been sent
        farm_entry = FarmDirectory.objects.get(account=self.user)

        # Assertions
        self.assertEqual(res.status_code, 200)
        self.assertEqual(res.json()['success'], True, "Valid token should return a success flag")
        self.assertEqual(res.json()['responseMessage'], "profile update successful")

        for i in edit_data:
            # Compare the before update user values with the current user values after the request has been sent
            try:
                before_data = getattr(self.user, i)
                after_data = getattr(user, i)
            except AttributeError:
                before_data = getattr(self.farm_entry, i)
                after_data = getattr(farm_entry, i)
            self.assertNotEqual(before_data, after_data, f"{i} field was not changed.\nThe user field should be updated to the given value")

    def test_valid_token_with_empty_params(self):
        """
        Tests if the server returns a descriptive message when served with an empty post data
        """
        edit_data = {}
        res = self.client.post(self.endpoint, data=edit_data, headers=self.headers, format="json")
        json_res = res.json()
        self.assertEqual(res.status_code, 400)
        self.assertEqual(json_res["success"], False, "Empty parameter should not return a success flag")
        self.assertEqual(json_res['responseMessage'], "profile update failed")

    def test_for_uneditable_fields(self):
        edit_data = {
            "username": "Edited Username",
            "bvn": 19028939309303,
            "nin": 999222000111,
        }
        res = self.client.post(self.endpoint, data=edit_data, headers=self.headers, format="json")
        # Get the user table after update request has been sent
        user = Account.objects.get_by_natural_key(self.user.username)
        # Get the farm directory user record after the update request has been sent
        farm_entry = FarmDirectory.objects.get(account=self.user)
        json_res = res.json()
        print(json_res)
        self.assertEqual(res.status_code, 400)
        self.assertEqual(json_res["success"], False, "Empty parameter should not return a success flag")
        self.assertEqual(json_res['responseMessage'], "profile update failed")
        for i in edit_data:
            # Compare the before update user values with the current user values after the request has been sent
            try:
                before_data = getattr(self.user, i)
                after_data = getattr(user, i)
            except AttributeError:
                before_data = getattr(self.farm_entry, i)
                after_data = getattr(farm_entry, i)
            self.assertEqual(before_data, after_data, f"{i} field was changed.\nThe user field should NOT be updated to the given value")


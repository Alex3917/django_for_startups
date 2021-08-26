# Standard Library imports

# Core Django imports
from django.test import TestCase

# Third-party imports
from rest_framework.test import APIRequestFactory, force_authenticate

# App imports
import app.views.account_management_views
from utils.test_utils import *
from app.models import User


class UserTestCase(TestCase):
    def setUp(self):
        self.factory = APIRequestFactory()
        self.view = app.views.account_management_views.User.as_view()

        self.maxDiff = None

    ########
    # POST #
    ########
    def test_valid_signup(self):
        post_request_data = {
            "username": "aoeu",
            "email_address": "example@example.com",
            "password": "hunter2!",
            "terms_of_service_accepted": True,
        }

        request = self.factory.post("/user", post_request_data)
        with self.assertNumQueries(18):
            resp = self.view(request)

        self.assertEqual(201, resp.status_code)
        self.assertIn("auth_token", resp.data["data"])

        self.assertEqual(1, User.objects.count())
        self.assertEqual(1, EmailAddress.objects.count())

    def test_usernames_cant_be_longer_than_15_chars(self):
        post_request_data = {
            "username": "aoeuaoeuaoeuaoeu",
            "email_address": "example@example.com",
            "password": "hunter2!",
            "terms_of_service_accepted": True,
        }

        request = self.factory.post("/user", post_request_data)
        with self.assertNumQueries(0):
            resp = self.view(request)

        expected_resp = {
            "errors": {
                "display_error": "",
                "field_errors": {
                    "username": [
                        "Usernames must be less than or equal to 15 characters."
                    ]
                },
            }
        }

        self.assertEqual(422, resp.status_code)
        self.assertEqual(expected_resp, resp.data)

        self.assertEqual(0, User.objects.count())
        self.assertEqual(0, EmailAddress.objects.count())

    def test_username_must_start_with_a_letter(self):
        post_request_data = {
            "username": "1aoeu",
            "email_address": "example@example.com",
            "password": "hunter2!",
            "terms_of_service_accepted": True,
        }

        request = self.factory.post("/user", post_request_data)
        with self.assertNumQueries(0):
            resp = self.view(request)

        expected_resp = {
            "errors": {
                "display_error": "",
                "field_errors": {
                    "username": [
                        "Username must start with a letter, and contain only letters, numbers, and underscores."
                    ]
                },
            }
        }

        self.assertEqual(422, resp.status_code)
        self.assertEqual(expected_resp, resp.data)

        self.assertEqual(0, User.objects.count())
        self.assertEqual(0, EmailAddress.objects.count())

    def test_password_must_be_at_least_8_characters(self):
        post_request_data = {
            "username": "aoeu",
            "email_address": "example@example.com",
            "password": "aoeu",
            "terms_of_service_accepted": True,
        }

        request = self.factory.post("/user", post_request_data)
        with self.assertNumQueries(0):
            resp = self.view(request)

        expected_resp = {
            "errors": {
                "display_error": "",
                "field_errors": {"password": ["Shorter than minimum length 8."]},
            }
        }

        self.assertEqual(422, resp.status_code)
        self.assertEqual(expected_resp, resp.data)

        self.assertEqual(0, User.objects.count())
        self.assertEqual(0, EmailAddress.objects.count())

    def test_must_enter_a_valid_email_address(self):
        post_request_data = {
            "username": "aoeu",
            "email_address": "example@@example.com",
            "password": "hunter2!",
            "terms_of_service_accepted": True,
        }

        request = self.factory.post("/user", post_request_data)
        with self.assertNumQueries(0):
            resp = self.view(request)

        expected_resp = {
            "errors": {
                "display_error": "",
                "field_errors": {"email_address": ["Not a valid email address."]},
            }
        }

        self.assertEqual(422, resp.status_code)
        self.assertEqual(expected_resp, resp.data)

        self.assertEqual(0, User.objects.count())
        self.assertEqual(0, EmailAddress.objects.count())

    def test_user_must_supply_all_required_fields(self):
        post_request_data = {}

        request = self.factory.post("/user", post_request_data)
        with self.assertNumQueries(0):
            resp = self.view(request)

        expected_resp = {
            "errors": {
                "display_error": "",
                "field_errors": {
                    "email_address": ["Not a valid email address."],
                    "password": ["Shorter than minimum length 8."],
                    "terms_of_service": ["Field may not be null."],
                    "username": [
                        "Usernames must be less than or equal to 15 characters.",
                        "Username must start with a letter, and contain only letters, numbers, and underscores.",
                    ],
                },
            }
        }

        self.assertEqual(422, resp.status_code)
        self.assertEqual(expected_resp, resp.data)

        self.assertEqual(0, User.objects.count())
        self.assertEqual(0, EmailAddress.objects.count())

    def test_user_must_accept_terms_of_service(self):
        post_request_data = {
            "username": "aoeu",
            "email_address": "example@example.com",
            "password": "hunter2!",
            "terms_of_service_accepted": False,
        }

        request = self.factory.post("/user", post_request_data)
        with self.assertNumQueries(2):
            resp = self.view(request)

        expected_resp = {
            "errors": {
                "display_error": "You must accept the terms of service in order to use example.com!",
                "internal_error_code": 42901,
            }
        }

        self.assertEqual(429, resp.status_code)
        self.assertEqual(expected_resp, resp.data)

        self.assertEqual(0, User.objects.count())
        self.assertEqual(0, EmailAddress.objects.count())

    def test_user_cannot_create_an_account_with_a_username_thats_already_taken(self):
        UserFactory(
            username="aoeu", email_address="example@example.com", password="hunter2!"
        )

        post_request_data = {
            "username": "aoeu",
            "email_address": "example2@example.com",
            "password": "hunter2!",
            "terms_of_service_accepted": True,
        }

        request = self.factory.post("/user", post_request_data)
        with self.assertNumQueries(1):
            resp = self.view(request)

        expected_resp = {
            "errors": {
                "display_error": "An account with this username already exists!",
                "internal_error_code": 40901,
            }
        }

        self.assertEqual(409, resp.status_code)
        self.assertEqual(expected_resp, resp.data)

        self.assertEqual(1, User.objects.count())
        self.assertEqual(1, EmailAddress.objects.count())

    def test_accounts_with_unverified_primary_email_addresses_get_clobbered_by_new_signups(
        self,
    ):
        UserFactory(
            username="aoeu", email_address="example@example.com", password="hunter2!"
        )

        # Same email address
        post_request_data = {
            "username": "aoeu2",
            "email_address": "example@example.com",
            "password": "hunter2!",
            "terms_of_service_accepted": True,
        }

        request = self.factory.post("/user", post_request_data)
        with self.assertNumQueries(24):
            resp = self.view(request)

        self.assertEqual(201, resp.status_code)

        self.assertEqual(1, User.objects.count())
        self.assertEqual(1, EmailAddress.objects.count())

    #######
    # GET #
    #######
    def test_only_logged_in_users_can_access_endpoint_to_get_profile(self):
        # First create the user
        post_request_data = {
            "username": "Aoeu",
            "email_address": "Example@example.com",
            "password": "hunter2!",
            "terms_of_service_accepted": True,
        }

        request1 = self.factory.post("/user", post_request_data)
        with self.assertNumQueries(18):
            resp = self.view(request1)

        self.assertEqual(201, resp.status_code)

        # Next GET the user's profile
        request2 = self.factory.get("/user")
        with self.assertNumQueries(0):
            resp = self.view(request2)

        self.assertEqual(401, resp.status_code)

    def test_getting_user_profile(self):
        # First create the user
        post_request_data = {
            "username": "Aoeu",
            "email_address": "Example@example.com",
            "password": "hunter2!",
            "terms_of_service_accepted": True,
        }

        request1 = self.factory.post("/user", post_request_data)
        with self.assertNumQueries(18):
            resp = self.view(request1)

        self.assertEqual(201, resp.status_code)

        # Next GET the user's profile
        user_model = User.objects.all()[0]
        request2 = self.factory.get("/user")
        force_authenticate(request2, user=user_model)
        with self.assertNumQueries(2):
            resp = self.view(request2)

        self.assertEqual(200, resp.status_code)

        expected_resp = {
            "data": {
                "user_profile": {
                    "nfc_name": "",
                    "nfc_username": "Aoeu",
                    "nfkc_name": "",
                    "nfkc_primary_email_address": "example@example.com",
                    "nfkc_username": "aoeu",
                }
            }
        }

        resp.data["data"]["user_profile"].pop("date_joined")
        self.assertEqual(expected_resp, resp.data)

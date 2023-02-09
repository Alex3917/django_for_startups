# Standard Library imports

# Core Django imports
from django.test import TestCase

# Third-party imports
from rest_framework.test import APIRequestFactory

# App imports
from app.views import account_management_views
from utils.test_utils import *


class LoginTestCase(TestCase):
    def setUp(self):
        self.username = 'aoeu'
        self.email_address = 'example@example.com'
        self.password = 'hunter2!'

        self.factory = APIRequestFactory()
        self.view1 = account_management_views.CustomTokenObtainPairView.as_view()
        self.view2 = account_management_views.User.as_view()

        # Create user1
        self.user1 = UserFactory(username=self.username, email_address=self.email_address, password=self.password)

        self.maxDiff = None

    ########
    # POST #
    ########
    def test_user_can_log_into_site_with_username(self):
        post_request_data = {'nfkc_username': self.username, 'password': self.password}

        request1 = self.factory.post('/api-token-auth/', post_request_data)

        with self.assertNumQueries(1):
            resp = self.view1(request1)


        self.assertEqual(200, resp.status_code)

        auth_token = resp.data['access']
        auth_header_value = f'JWT {auth_token}'

        request2 = self.factory.get('/account_management/user/', HTTP_AUTHORIZATION=auth_header_value)
        with self.assertNumQueries(3):
            resp = self.view2(request2)

        self.assertEqual(resp.status_code, 200)

    def test_user_can_log_into_site_with_uppercase_username(self):
        post_request_data = {'nfkc_username': self.username.upper(), 'password': self.password}

        request1 = self.factory.post('/api-token-auth/', post_request_data)

        with self.assertNumQueries(1):
            resp = self.view1(request1)


        self.assertEqual(200, resp.status_code)

        auth_token = resp.data['access']
        auth_header_value = f'JWT {auth_token}'

        request2 = self.factory.get('/account_management/user/', HTTP_AUTHORIZATION=auth_header_value)
        with self.assertNumQueries(3):
            resp = self.view2(request2)

        self.assertEqual(resp.status_code, 200)

    def test_user_can_log_into_site_with_email_adress(self):
        post_request_data = {'nfkc_username': self.email_address, 'password': self.password}

        request1 = self.factory.post('/api-token-auth/', post_request_data)

        with self.assertNumQueries(2):
            resp = self.view1(request1)


        self.assertEqual(200, resp.status_code)

        auth_token = resp.data['access']
        auth_header_value = f'JWT {auth_token}'

        request2 = self.factory.get('/account_management/user/', HTTP_AUTHORIZATION=auth_header_value)
        with self.assertNumQueries(3):
            resp = self.view2(request2)

        self.assertEqual(resp.status_code, 200)

    def test_user_can_log_into_site_with_uppercase_email_adress(self):
        post_request_data = {'nfkc_username': self.email_address.upper(), 'password': self.password}

        request1 = self.factory.post('/api-token-auth/', post_request_data)

        with self.assertNumQueries(2):
            resp = self.view1(request1)


        self.assertEqual(200, resp.status_code)

        auth_token = resp.data['access']
        auth_header_value = f'JWT {auth_token}'

        request2 = self.factory.get('/account_management/user/', HTTP_AUTHORIZATION=auth_header_value)
        with self.assertNumQueries(3):
            resp = self.view2(request2)

        self.assertEqual(resp.status_code, 200)
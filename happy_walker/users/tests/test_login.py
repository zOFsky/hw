from django.test import TestCase, Client
from django.urls import reverse
import json
import mock
from .methods_for_test import MethodsForTest

class LoginTest(TestCase):

    def setUpTestData(self):
        self.registration_url = reverse('register')
        self.confirm_email_url = reverse('confirm_email')
        self.login_url = reverse('login')

    def setUp(self):
        self.client = Client()
        print("----------{}-----------".format(self._testMethodName))

    methods = MethodsForTest()

    @mock.patch("users.tokens.TokenGenerator.check_token", methods.fake_check_token)
    def test_login_api_with_correct_data_input(self):
        request_data = self.methods.create_json_request(username='username1', password='abc1234',
                                                email='asd@mail.com', first_name='r', last_name='r')
        resp = self.client.post(self.registration_url, request_data,
             content_type="application/json")
        self.assertEqual(resp.status_code, 201)
        resp = json.loads(resp.content)
        email = self.methods.create_json_request(uid=str(resp['uid']), token='true')
        resp2 = self.client.post(self.confirm_email_url, email,
                                 content_type="application/json")
        self.assertEqual(resp2.status_code, 200)
        login_data = self.methods.create_json_request(username_or_email='username1',
                             password='abc1234')
        resp3 = self.client.post(self.login_url, login_data,
                                 content_type="application/json")
        self.assertEqual(resp3.status_code, 230)

    @mock.patch("users.tokens.TokenGenerator.check_token", methods.fake_check_token)
    def test_login_with_no_password(self):
        request_data = self.methods.create_json_request(username='username1', password='abc1234',
                                                email='asd@mail.com', first_name='r', last_name='r')
        resp = self.client.post(self.registration_url, request_data,
                                content_type="application/json")
        self.assertEqual(resp.status_code, 201)
        resp = json.loads(resp.content)
        email = self.methods.create_json_request(uid=str(resp['uid']), token='true')
        resp2 = self.client.post(self.confirm_email_url, email,
                                 content_type="application/json")
        self.assertEqual(resp2.status_code, 200)
        login_data = self.methods.create_json_request(username_or_email='username1',
                             password='')
        resp3 = self.client.post(self.login_url, login_data,
                                 content_type="application/json")
        self.assertEqual(resp3.status_code, 400)

    @mock.patch("users.tokens.TokenGenerator.check_token", methods.fake_check_token)
    def test_login_with_email(self):
        request_data = self.methods.create_json_request(username='username1', password='abc1234',
                                                email='asd@mail.com', first_name='r', last_name='r')
        resp = self.client.post(self.registration_url, request_data,
             content_type="application/json")
        self.assertEqual(resp.status_code, 201)
        resp = json.loads(resp.content)
        email = self.methods.create_json_request(uid=str(resp['uid']), token='true')
        resp2 = self.client.post(self.confirm_email_url, email,
                                 content_type="application/json")
        self.assertEqual(resp2.status_code, 200)
        login_data = self.methods.create_json_request(username_or_email='asd@mail.com',
                             password='abc1234')
        resp3 = self.client.post(self.login_url, login_data,
                                 content_type="application/json")
        self.assertEqual(resp3.status_code, 230)

    def test_login_with_empty_data(self):
        login_data = self.methods.create_json_request(username_or_email=None,
                             password=None)
        resp2 = self.client.post(self.login_url, login_data, 
                                 content_type="application/json")
        self.assertEqual(resp2.status_code, 400)

    @mock.patch("users.tokens.TokenGenerator.check_token", methods.fake_check_token)
    def test_login_with_wrong_password(self):
        request_data = self.methods.create_json_request(username='username1', password='abc1234',
                                                email='asd@mail.com', first_name='r', last_name='r')
        resp = self.client.post(self.registration_url, request_data,
             content_type="application/json")
        self.assertEqual(resp.status_code, 201)
        resp = json.loads(resp.content)
        email = self.methods.create_json_request(uid=str(resp['uid']), token='true')
        resp2 = self.client.post(self.confirm_email_url, email,
                                 content_type="application/json")
        self.assertEqual(resp2.status_code, 200)
        login_data = self.methods.create_json_request(username_or_email='username1',
                             password='abcd1234')
        resp3 = self.client.post(self.login_url, login_data,
                                 content_type="application/json")
        self.assertEqual(resp3.status_code, 467)

    def test_login_with_no_email_or_username(self):
        request_data = self.methods.create_json_request(password='abc4234')
        resp = self.client.post(self.login_url, request_data,
             content_type="application/json")
        self.assertEqual(resp.status_code, 400)

    def test_login_user_does_not_exists(self):
        request_data = self.methods.create_json_request(username_or_email='username1',
                                                         password='password')
        resp = self.client.post(self.login_url, request_data,
             content_type="application/json")
        self.assertEqual(resp.status_code, 432)


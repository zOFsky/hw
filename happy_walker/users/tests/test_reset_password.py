from django.test import TestCase, Client
from django.urls import reverse
import json
import mock
from .methods_for_test import MethodsForTest

class LoginTest(TestCase):

    def setUpTestData(self):
        self.registration_url = reverse('register')
        self.confirm_email_url = reverse('confirm_email')
        self.reset_url = reverse('reset_password')

    def setUp(self):
        self.client = Client()
        print("*+*+*+*+*+*+*+*+*{}*+*+*+*+*+*+*+*+*+*".format(self._testMethodName))

    methods = MethodsForTest()

    @mock.patch("users.tokens.TokenGenerator.check_token", methods.fake_check_token)
    def test_reset_pass_api_with_correct_data_input(self):
        request_data = self.methods.create_json_request(username='username1', password='abc12345',
                                email='asd@mail.com', last_name="Smith", first_name="John")
        resp = self.client.post(self.registration_url, request_data,
             content_type="application/json")
        self.assertEqual(resp.status_code, 201)
        resp_content = json.loads(resp.content)
        email = self.methods.create_json_request(uid=resp_content['uid'], token='true')
        resp2 = self.client.post(self.confirm_email_url, email,
                                 content_type="application/json")
        self.assertEqual(resp2.status_code, 200)
        reset_data = self.methods.create_json_request(uid=resp_content['uid'], token='true',
                             password='new_password', repeat_password='new_password')
        resp3 = self.client.post(self.reset_url, reset_data,
                                 content_type="application/json")
        self.assertEqual(resp3.status_code, 201)

    @mock.patch("users.tokens.TokenGenerator.check_token", methods.fake_check_token)
    def test_reset_pass_api_with_no_password(self):
        request_data = self.methods.create_json_request(username='username1', password='abc12345',
                                email='asd@mail.com', last_name="Smith", first_name="John")
        resp = self.client.post(self.registration_url, request_data,
             content_type="application/json")
        self.assertEqual(resp.status_code, 201)
        resp_content = json.loads(resp.content)
        email = self.methods.create_json_request(uid=resp_content['uid'], token='true')
        resp2 = self.client.post(self.confirm_email_url, email,
                                 content_type="application/json")
        self.assertEqual(resp2.status_code, 200)
        reset_data = self.methods.create_json_request(uid=resp_content['uid'], token='true',
                            repeat_password='new_password')
        resp3 = self.client.post(self.reset_url, reset_data,
                                 content_type="application/json")
        self.assertEqual(resp3.status_code, 400)

    @mock.patch("users.tokens.TokenGenerator.check_token", methods.fake_check_token)
    def test_reset_pass_api_with_missmatched_password(self):
        request_data = self.methods.create_json_request(username='username1', password='abc12345',
                                email='asd@mail.com', last_name="Smith", first_name="John")
        resp = self.client.post(self.registration_url, request_data,
             content_type="application/json")
        self.assertEqual(resp.status_code, 201)
        resp_content = json.loads(resp.content)
        email = self.methods.create_json_request(uid=resp_content['uid'], token='true')
        resp2 = self.client.post(self.confirm_email_url, email,
                                 content_type="application/json")
        self.assertEqual(resp2.status_code, 200)
        reset_data = self.methods.create_json_request(uid=resp_content['uid'], token='true',
                             password='new_password', repeat_password='missmatched')
        resp3 = self.client.post(self.reset_url, reset_data,
                                 content_type="application/json")
        self.assertEqual(resp3.status_code, 444)

    
    @mock.patch("users.tokens.TokenGenerator.check_token", methods.fake_check_token)
    def test_reset_pass_api_with_incorrect_userid(self):
        request_data = self.methods.create_json_request(username='username1', password='abc12345',
                                email='asd@mail.com', last_name="Smith", first_name="John")
        resp = self.client.post(self.registration_url, request_data,
             content_type="application/json")
        self.assertEqual(resp.status_code, 201)
        resp_content = json.loads(resp.content)
        email = self.methods.create_json_request(uid=resp_content['uid'], token='true')
        resp2 = self.client.post(self.confirm_email_url, email,
                                 content_type="application/json")
        self.assertEqual(resp2.status_code, 200)
        reset_data = self.methods.create_json_request(uid=5555, token='true',
                             password='new_password', repeat_password='new_password')
        resp3 = self.client.post(self.reset_url, reset_data,
                                 content_type="application/json")
        self.assertEqual(resp3.status_code, 404)

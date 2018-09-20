from django.test import TestCase, Client
from django.urls import reverse
import json
import mock
from .methods_for_test import MethodsForTest

class LoginTest(TestCase):

    def setUpTestData(self):
        self.registration_url = reverse('register')
        self.confirm_email_url = reverse('confirm_email')
        self.forgot_url = reverse('forgot_password')

    def setUp(self):
        self.client = Client()
        print("-^-^-^-^-^-^-^-^-^-{}-^-^-^-^-^-^-^-^-^-^-".format(self._testMethodName))

    methods = MethodsForTest()

    @mock.patch("users.tokens.TokenGenerator.check_token", methods.fake_check_token)
    def test_forgot_password_api_with_correct_data_input(self):
        request_data = self.methods.create_json_request(username='username1', password='abc12345',
                                                        email='asd@mail.com', last_name="Smith", first_name="John")
        resp = self.client.post(self.registration_url, request_data,
             content_type="application/json")
        self.assertEqual(resp.status_code, 201)
        resp = json.loads(resp.content)
        email = self.methods.create_json_request(uid=str(resp['uid']), token='true')
        resp2 = self.client.post(self.confirm_email_url, email,
                                 content_type="application/json")
        self.assertEqual(resp2.status_code, 200)
        forgot_data = self.methods.create_json_request(email='asd@mail.com')
        resp3 = self.client.post(self.forgot_url, forgot_data,
                                 content_type="application/json")
        self.assertEqual(resp3.status_code, 202)

    @mock.patch("users.tokens.TokenGenerator.check_token", methods.fake_check_token)
    
    def test_forgot_pass_with_empty_data(self):
        forgot_data = self.methods.create_json_request(email=None)
        resp2 = self.client.post(self.forgot_url, forgot_data, 
                                 content_type="application/json")
        self.assertEqual(resp2.status_code, 400)

    @mock.patch("users.tokens.TokenGenerator.check_token", methods.fake_check_token)
    def test_forgot_pass_with_email_not_in_db(self):
        forgot_data = self.methods.create_json_request(email='mail@some.com')
        resp3 = self.client.post(self.forgot_url, forgot_data,
                                 content_type="application/json")
        self.assertEqual(resp3.status_code, 200)




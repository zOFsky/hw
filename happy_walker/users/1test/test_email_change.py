from django.test import TestCase, Client
from django.urls import reverse
import json
import mock
from .methods_for_test import MethodsForTest

class UpdateTest(TestCase):

    def setUpTestData(self):
        self.registration_url = reverse('register')
        self.confirm_email_url = reverse('confirm_email')
        self.login_url = reverse('login')
        self.update_url = reverse('profile', args=['me'])
        self.change_email_url = reverse('change_email')

    def setUp(self):
        self.client = Client()
        print("-+-+-+-+-+-+-+-+-+-{}-+-+-+-+-+-+-+-+-+-+-".format(self._testMethodName))

    methods = MethodsForTest()

    @mock.patch("users.tokens.TokenGenerator.check_token", methods.fake_check_token)
    def test_email_change_with_correct_email(self):
        request_data = self.methods.create_json_request(username='username1', password='abc12345',
                                                        email='asd@mail.com', last_name="Smith", first_name="John")
        resp = self.client.post(self.registration_url, request_data,
             content_type="application/json")
        self.assertEqual(resp.status_code, 201)
        resp = json.loads(resp.content)
        email = self.methods.create_json_request(uid=resp['uid'], token='true')
        resp_confirm_email = self.client.post(self.confirm_email_url, email,
                                              content_type="application/json")
        self.assertEqual(resp_confirm_email.status_code, 200)
        login_data = self.methods.create_json_request(username_or_email='username1',
                             password='abc12345')
        resp2 = self.client.post(self.login_url, login_data, 
                                 content_type="application/json")
        self.assertEqual(resp2.status_code, 230)
        update_data = self.methods.create_json_request(first_name="Jane", email="asd@fun.com", last_name="Doe")
        resp3 = self.client.post(self.update_url,update_data,
                                 content_type="application/json")
        self.assertEqual(resp3.status_code, 202)
        change_mail_data = self.methods.create_json_request(token='true',
                                  uid=resp['uid'], new_email="new@mail.com")
        resp_email_changer = self.client.post(self.change_email_url, change_mail_data,
                                 content_type="application/json")
        self.assertEqual(resp_email_changer.status_code, 201)

    @mock.patch("users.tokens.TokenGenerator.check_token", methods.fake_check_token)
    def test_email_change_with_incorrect_email(self):
        request_data = self.methods.create_json_request(username='username1', password='abc12345',
                                                        email='asd@mail.com', last_name="Smith", first_name="John")
        resp = self.client.post(self.registration_url, request_data,
             content_type="application/json")
        self.assertEqual(resp.status_code, 201)
        resp = json.loads(resp.content)
        email = self.methods.create_json_request(uid=resp['uid'], token='true')
        resp_confirm_email = self.client.post(self.confirm_email_url, email,
                                              content_type="application/json")
        self.assertEqual(resp_confirm_email.status_code, 200)
        login_data = self.methods.create_json_request(username_or_email='username1',
                             password='abc12345')
        resp2 = self.client.post(self.login_url, login_data,
                                 content_type="application/json")
        self.assertEqual(resp2.status_code, 230)
        update_data = self.methods.create_json_request(first_name="Andriy", email="asd@fun.com",
                   last_name="Doe")
        resp3 = self.client.post(self.update_url,update_data,
                                 content_type="application/json")
        self.assertEqual(resp3.status_code, 202)
        change_mail_data = self.methods.create_json_request(token='true',
                                  uid=resp['uid'], new_email="new@mailcom")
        resp_email_changer = self.client.post(self.change_email_url, change_mail_data,
                                 content_type="application/json")
        self.assertEqual(resp_email_changer.status_code, 400)

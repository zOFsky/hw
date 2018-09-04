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

    def setUp(self):
        self.client = Client()
        print("----------{}-----------".format(self._testMethodName))

    methods = MethodsForTest()

    @mock.patch("users.tokens.TokenGenerator.check_token", methods.fake_check_token)
    def test_update_api_with_correct_data_input(self):
        request_data = self.methods.create_json_request(username='username1', password='abc1234',
                                                        email='asd@mail.com', last_name="Smith", first_name="John")
        resp = self.client.post(self.registration_url, request_data,
             content_type="application/json")
        self.assertEqual(resp.status_code, 201)
        resp = json.loads(resp.content)
        email = self.methods.create_json_request(uid=str(resp['uid']), token='true')
        resp_confirm_email = self.client.post(self.confirm_email_url, email,
                                 content_type="application/json")
        self.assertEqual(resp_confirm_email.status_code, 200)
        login_data = self.methods.create_json_request(username_or_email='username1',
                             password='abc1234')
        resp2 = self.client.post(self.login_url, login_data, 
                                 content_type="application/json")
        self.assertEqual(resp2.status_code, 230)
        update_data = self.methods.create_json_request(first_name="Andriy", last_name="Staythere",
                                email="asd@mail.com")
        resp3 = self.client.post(self.update_url,update_data,
                                 content_type="application/json")
        self.assertEqual(resp3.status_code, 201)

    @mock.patch("users.tokens.TokenGenerator.check_token", methods.fake_check_token)
    def test_update_api_with_incorrect_email(self):
        request_data = self.methods.create_json_request(username='username1', password='abc1234',
                                                        email='asd@mail.com', last_name="Smith", first_name="John")
        resp = self.client.post(self.registration_url, request_data,
             content_type="application/json")
        self.assertEqual(resp.status_code, 201)
        resp = json.loads(resp.content)
        email = self.methods.create_json_request(uid=str(resp['uid']), token='true')
        resp_confirm_email = self.client.post(self.confirm_email_url, email,
                                              content_type="application/json")
        self.assertEqual(resp_confirm_email.status_code, 200)
        login_data = self.methods.create_json_request(username_or_email='username1',
                             password='abc1234')
        resp2 = self.client.post(self.login_url, login_data, 
                                 content_type="application/json")
        self.assertEqual(resp2.status_code, 230)
        update_data = self.methods.create_json_request(first_name="Andriy", last_name="Staythere", email='123')
        resp3 = self.client.post(self.update_url, update_data,
                                 content_type="application/json")
        self.assertEqual(resp3.status_code, 400)

    def test_update_api_by_anonym_user(self):
        update_data = self.methods.create_json_request(first_name="Andriy", last_name="Staythere", email='123@er.rt')
        resp3 = self.client.post(self.update_url, update_data,
                                 content_type="application/json")
        self.assertEqual(resp3.status_code, 302)

    @mock.patch("users.tokens.TokenGenerator.check_token", methods.fake_check_token)
    def test_update_api_with_correct_data_checking_functionality(self):
        request_data = self.methods.create_json_request(username='username1', password='abc1234',
                                                        email='asd@mail.com', last_name="Smith", first_name="John")
        resp = self.client.post(self.registration_url, request_data,
             content_type="application/json")
        self.assertEqual(resp.status_code, 201)
        resp = json.loads(resp.content)
        email = self.methods.create_json_request(uid=str(resp['uid']), token='true')
        resp_confirm_email = self.client.post(self.confirm_email_url, email,
                                              content_type="application/json")
        self.assertEqual(resp_confirm_email.status_code, 200)
        login_data = self.methods.create_json_request(username_or_email='username1',
                             password='abc1234')
        resp2 = self.client.post(self.login_url, login_data, 
                                 content_type="application/json")
        self.assertEqual(resp2.status_code, 230)
        update_data = self.methods.create_json_request(first_name="Andriy", last_name="Doe",
                    email="asd@mail.com")
        resp3 = self.client.post(self.update_url, update_data,
                                 content_type="application/json")
        self.assertEqual(resp3.status_code, 201)

    @mock.patch("users.tokens.TokenGenerator.check_token", methods.fake_check_token)
    def test_update_api_with_correct_email(self):
        request_data = self.methods.create_json_request(username='username1', password='abc1234',
                                                        email='asd@mail.com', last_name="Smith", first_name="John")
        resp = self.client.post(self.registration_url, request_data,
             content_type="application/json")
        self.assertEqual(resp.status_code, 201)
        resp = json.loads(resp.content)
        email = self.methods.create_json_request(uid=str(resp['uid']), token='true')
        resp_confirm_email = self.client.post(self.confirm_email_url, email,
                                              content_type="application/json")
        self.assertEqual(resp_confirm_email.status_code, 200)
        login_data = self.methods.create_json_request(username_or_email='username1',
                             password='abc1234')
        resp2 = self.client.post(self.login_url, login_data, 
                                 content_type="application/json")
        self.assertEqual(resp2.status_code, 230)
        update_data = self.methods.create_json_request(first_name="Andriy", email="asd@fun.com", last_name="Doe")
        resp3 = self.client.post(self.update_url, update_data,
                                 content_type="application/json")
        self.assertEqual(resp3.status_code, 202)

    @mock.patch("users.tokens.TokenGenerator.check_token", methods.fake_check_token)
    def test_update_api_with_incorrect_email(self):
        request_data = self.methods.create_json_request(username='username1', password='abc1234',
                                                        email='asd@mail.com', last_name="Smith", first_name="John")
        resp = self.client.post(self.registration_url, request_data,
             content_type="application/json")
        self.assertEqual(resp.status_code, 201)
        resp = json.loads(resp.content)
        email = self.methods.create_json_request(uid=str(resp['uid']), token='true')
        resp_confirm_email = self.client.post(self.confirm_email_url, email,
                                              content_type="application/json")
        self.assertEqual(resp_confirm_email.status_code, 200)
        login_data = self.methods.create_json_request(username_or_email='username1',
                             password='abc1234')
        resp2 = self.client.post(self.login_url, login_data, 
                                 content_type="application/json")
        self.assertEqual(resp2.status_code, 230)
        update_data = self.methods.create_json_request(first_name="Andriy", email="asd@funcom", last_name="Doe")
        resp3 = self.client.post(self.update_url, update_data,
                                 content_type="application/json")
        self.assertEqual(resp3.status_code, 400)

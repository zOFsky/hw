from django.contrib.auth.models import User
from django.test import TestCase, RequestFactory, Client
from django.urls import reverse, resolve
from home.views import homepage
from users.views import UserRegister
from django.http import HttpRequest
import json

class UpdateTest(TestCase):

  
    def setUp(self):
        self.registration_url = reverse('register')
        self.login_url = reverse('login')
        self.update_url = reverse('update')
        self.client = Client()
        print("----------{}-----------".format(self._testMethodName))

    def create_json_request(self, username="", password="", email="",
                    first_name="", last_name="", username_or_email=""):
        my_dict = {
            "username": username,
            "password": password,
            "email": email,
            "first_name": first_name,
            "last_name": last_name,
            "username_or_email": username_or_email,
    
        }
        json_string = json.dumps(my_dict)
        return json_string

    
    def test_update_api_with_correct_data_input(self):
        request_data = self.create_json_request('username1', 'abc1234', 'asd@mail.com')
        resp = self.client.post(self.registration_url, request_data,
             content_type="application/json")
        self.assertEqual(resp.status_code, 201)
        login_data = self.create_json_request(username_or_email='username1',
                             password='abc1234')
        resp2 = self.client.post(self.login_url, login_data, 
                                 content_type="application/json")
        self.assertEqual(resp2.status_code, 230)
        update_data = self.create_json_request(first_name="Andriy", last_name="Staythere")
        resp3 = self.client.put(self.update_url,update_data,
                                 content_type="application/json")
        self.assertEqual(resp.status_code, 201)
    
    # def test_login_with_no_password(self):
    #     request_data = self.create_json_request('username1', 'abc1234', 'asd@mail.com')
    #     resp = self.client.post(self.registration_url, request_data,
    #          content_type="application/json")
    #     self.assertEqual(resp.status_code, 201)
    #     login_data = self.create_json_request(username_or_email='username1',
    #                          password='')
    #     resp2 = self.client.post(self.login_url, login_data, 
    #                              content_type="application/json")
    #     self.assertEqual(resp2.status_code, 400)

    # def test_login_with_email(self):
    #     request_data = self.create_json_request('username1', 'abc1234', 'asd@mail.com')
    #     resp = self.client.post(self.registration_url, request_data,
    #          content_type="application/json")
    #     self.assertEqual(resp.status_code, 201)
    #     login_data = self.create_json_request(username_or_email='asd@mail.com',
    #                          password='abc1234')
    #     resp2 = self.client.post(self.login_url, login_data, 
    #                              content_type="application/json")
    #     self.assertEqual(resp2.status_code, 230)
    
    # def test_login_with_empty_data(self):
    #     login_data = self.create_json_request(username_or_email=None,
    #                          password=None)
    #     resp2 = self.client.post(self.login_url, login_data, 
    #                              content_type="application/json")
    #     self.assertEqual(resp2.status_code, 400)

    # def test_login_with_wrong_password(self):
    #     request_data = self.create_json_request('username1', 'abc1234', 'asd@mail.com')
    #     resp = self.client.post(self.registration_url, request_data,
    #          content_type="application/json")
    #     self.assertEqual(resp.status_code, 201)
    #     login_data = self.create_json_request(username_or_email='username1',
    #                          password='abcd1234')
    #     resp2 = self.client.post(self.login_url, login_data, 
    #                              content_type="application/json")
    #     self.assertEqual(resp2.status_code, 467)
    

    # def test_login_with_no_email_or_username(self):
    #     request_data = self.create_json_request(password='abc4234')
    #     resp = self.client.post(self.login_url, request_data,
    #          content_type="application/json")
    #     self.assertEqual(resp.status_code, 400)

    # def test_login_user_does_not_exists(self):
    #     request_data = self.create_json_request(username_or_email='username1',
    #                                                      password='password')
    #     resp = self.client.post(self.login_url, request_data,
    #          content_type="application/json")
    #     self.assertEqual(resp.status_code, 432)


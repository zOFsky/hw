from django.contrib.auth.models import User
from django.test import TestCase, RequestFactory, Client
from django.urls import reverse, resolve
from home.views import homepage
from users.views import UserRegister
from django.http import HttpRequest
import json

class RegisterTest(TestCase):

  
    def setUp(self):
        self.registration_url = reverse('register')
        self.client = Client()
        print("~~~~~~{}~~~~~~~".format(self._testMethodName))

    def create_json_request(self, username="", password="", email="",
                    firstname="", lastname=""):
        my_dict = {
            "username": username,
            "password": password,
            "email": email,
            "firstname": firstname,
            "lastname": lastname
        }
        json_string = json.dumps(my_dict)
        return json_string

    def test_go_home(self):
        found = resolve('/')
        self.assertEqual(found.func, homepage)

    def test_home_returns_correct_html(self):
        request = HttpRequest()
        response = homepage(request)
        html = response.content.decode('utf8')
        self.assertTrue(html.startswith('Here'))
        self.assertTrue(html.endswith('ting'))

    
    def test_registration_api_with_correct_data_input(self):
        request_data = self.create_json_request('username1', 'abc1234', 'asd@mail.com')
        resp = self.client.post(self.registration_url, request_data,
             content_type="application/json")
        self.assertEqual(resp.status_code, 201)
    
    def test_registration_with_password_too_short(self):
        request_data = self.create_json_request('username2', 'abc14', 'basd@mail.com')
        resp = self.client.post(self.registration_url, request_data,
             content_type="application/json")
        #print("MESSAGE: {}".format(resp))
        self.assertEqual(resp.status_code, 400)
    
    def test_registration_with_incorrect_email(self):
        request_data = self.create_json_request('username3', 'abc1434', 'asd@mailcom')
        resp = self.client.post(self.registration_url, request_data,
             content_type="application/json")
        self.assertEqual(resp.status_code, 400)

    
    def test_registration_with_incorrect_email_and_password(self):
        request_data = self.create_json_request('username4', 'abc4', 'asdmailcom')
        resp = self.client.post(self.registration_url, request_data,
             content_type="application/json")
        self.assertEqual(resp.status_code, 400)

    def test_registration_with_empty_email_and_password(self):
        request_data = self.create_json_request('username4', 'abc1234', 'asdf')
        resp = self.client.post(self.registration_url, request_data,
             content_type="application/json")
        self.assertEqual(resp.status_code, 400)

    def test_registration_wih_no_password(self):
        request_data = self.create_json_request('username5', email='asd@mail.com')
        resp = self.client.post(self.registration_url, request_data,
             content_type="application/json")
        self.assertEqual(resp.status_code, 400)

    def test_registration_with_no_email(self):
        request_data = self.create_json_request('username6', 'abc4234')
        resp = self.client.post(self.registration_url, request_data,
             content_type="application/json")
        self.assertEqual(resp.status_code, 400)

    def test_registration_username_exists(self):
        request_data = self.create_json_request('username1', 'abc4234', 'email1@i.ua')
        resp = self.client.post(self.registration_url, request_data,
             content_type="application/json")
        
        request_data = self.create_json_request('username1', 'abc4234', 'email1@i.ua')
        resp = self.client.post(self.registration_url, request_data,
             content_type="application/json")
        self.assertEqual(resp.status_code, 460)


    def test_registration_with_correct_data_then_existing_username_and_email_correct_data(self):
        request_data = self.create_json_request('username1', 'abc4234', 'email1@i.ua')
        resp1 = self.client.post(self.registration_url, request_data,
             content_type="application/json")

        request_data = self.create_json_request('username1', 'abc14234', 'email1@22.ua')
        resp2 = self.client.post(self.registration_url, request_data,
             content_type="application/json")

        request_data = self.create_json_request('username2', 'abc14234', 'email1@i.ua')
        resp3 = self.client.post(self.registration_url, request_data,
             content_type="application/json")
        
        request_data = self.create_json_request('username2', 'abc14234', 'email221@22.ua')
        resp4 = self.client.post(self.registration_url, request_data,
             content_type="application/json")
        self.assertEqual(resp1.status_code, 201)
        self.assertEqual(resp2.status_code, 460)
        self.assertEqual(resp3.status_code, 460)
        self.assertEqual(resp4.status_code, 201)
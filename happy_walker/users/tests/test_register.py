from django.test import TestCase, Client
from django.urls import reverse, resolve
from home.views import homepage
from django.http import HttpRequest
import json
from .methods_for_test import MethodsForTest

class RegisterTest(TestCase):

    def setUpTestData(self):
        self.registration_url = reverse('register')

    def setUp(self):
        self.client = Client()
        print("~~~~~~{}~~~~~~~".format(self._testMethodName))

    def test_go_home(self):
        found = resolve('/')
        self.assertEqual(found.func, homepage)

    def test_home_returns_correct_html(self):
        request = HttpRequest()
        response = homepage(request)
        html = response.content.decode('utf8')
        self.assertTrue(html.startswith('Here'))
        self.assertTrue(html.endswith('ting'))

    methods = MethodsForTest()
    
    def test_registration_api_with_correct_data_input(self):
        request_data = self.methods.create_json_request(username='username1', password='abc1234',
                                                        email='asd@mail.com', first_name='r', last_name='r')
        resp = self.client.post(self.registration_url, request_data,
             content_type="application/json")
        self.assertEqual(resp.status_code, 201)
    
    def test_registration_with_password_too_short(self):
        request_data = self.methods.create_json_request(username='username1', password='abc1',
                                                        email='asd@mail.com', first_name='r', last_name='r')
        resp = self.client.post(self.registration_url, request_data,
             content_type="application/json")
        self.assertEqual(resp.status_code, 400)
    
    def test_registration_with_incorrect_email(self):
        request_data = self.methods.create_json_request(username='username1', password='abc1234',
                                                        email='asd@mailcom', first_name='r', last_name='r')
        resp = self.client.post(self.registration_url, request_data,
             content_type="application/json")
        self.assertEqual(resp.status_code, 400)

    
    def test_registration_with_incorrect_email_and_password(self):
        request_data = self.methods.create_json_request(username='username1', password='abc34',
                                                        email='asdmail.com', first_name='r', last_name='r')
        resp = self.client.post(self.registration_url, request_data,
             content_type="application/json")
        self.assertEqual(resp.status_code, 400)

    def test_registration_with_empty_email_and_password(self):
        request_data = self.methods.create_json_request(username='username1', password='',
                                                        email='', first_name='r', last_name='r')
        resp = self.client.post(self.registration_url, request_data,
             content_type="application/json")
        self.assertEqual(resp.status_code, 400)

    def test_registration_wih_no_password(self):
        request_data = self.methods.create_json_request(username='username1',
                                                        email='asd@mail.com', first_name='r', last_name='r')
        resp = self.client.post(self.registration_url, request_data,
             content_type="application/json")
        self.assertEqual(resp.status_code, 400)

    def test_registration_with_no_email(self):
        request_data = self.methods.create_json_request(username='username1', password='abc1234')
        resp = self.client.post(self.registration_url, request_data,
             content_type="application/json")
        self.assertEqual(resp.status_code, 400)

    def test_registration_username_exists(self):
        request_data = self.methods.create_json_request(username='username1', password='abc1234',
                                                        email='asd@mail.com', first_name='r', last_name='r')
        resp = self.client.post(self.registration_url, request_data,
             content_type="application/json")

        request_data = self.methods.create_json_request(username='username1', password='abc1234',
                                                        email='asd@mail.com', first_name='r', last_name='r')
        resp = self.client.post(self.registration_url, request_data,
             content_type="application/json")
        self.assertEqual(resp.status_code, 460)


    def test_registration_with_correct_data_then_existing_username_and_email_correct_data(self):
        request_data = self.methods.create_json_request(username='username1', password='abc1234',
                                                        email='asd@mail.com', first_name='r', last_name='r')
        resp1 = self.client.post(self.registration_url, request_data,
             content_type="application/json")

        request_data = self.methods.create_json_request(username='username1', password='abc1234',
                                                        email='asacsd@mail.com', first_name='r', last_name='r')
        resp2 = self.client.post(self.registration_url, request_data,
             content_type="application/json")

        request_data = self.methods.create_json_request(username='username2', password='abc1234',
                                                        email='asd@mail.com', first_name='r', last_name='r')
        resp3 = self.client.post(self.registration_url, request_data,
             content_type="application/json")

        request_data = self.methods.create_json_request(username='username2', password='abc1234',
                                                        email='asascd@mail.com', first_name='r', last_name='r')
        resp4 = self.client.post(self.registration_url, request_data,
             content_type="application/json")
        self.assertEqual(resp1.status_code, 201)
        self.assertEqual(resp2.status_code, 460)
        self.assertEqual(resp3.status_code, 460)
        self.assertEqual(resp4.status_code, 201)
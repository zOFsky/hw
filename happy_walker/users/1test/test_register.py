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
        request_data = self.methods.create_json_request(username='username1', password='abc12345',
                                        email='asd@mail.com', last_name="Smith", first_name="John")
        resp = self.client.post(self.registration_url, request_data,
             content_type="application/json")
        self.assertEqual(resp.status_code, 201)
    
    def test_registration_with_password_too_short(self):
        request_data = self.methods.create_json_request(username='username1', password='abc4',
                                        email='asd@mail.com', last_name="Smith", first_name="John")
        resp = self.client.post(self.registration_url, request_data,
             content_type="application/json")
        self.assertEqual(resp.status_code, 400)

    def test_registration_with_username_too_short(self):
        request_data = self.methods.create_json_request(username='1', password='abc4defg',
                                        email='asd@mail.com', last_name="Smith", first_name="John")
        resp = self.client.post(self.registration_url, request_data,
             content_type="application/json")
        self.assertEqual(resp.status_code, 400)

    
    def test_registration_with_username_wrong_char(self):
        request_data = self.methods.create_json_request(username='1der@pes', password='abc4defg',
                                        email='asd@mail.com', last_name="Smith", first_name="John")
        resp = self.client.post(self.registration_url, request_data,
             content_type="application/json")
        self.assertEqual(resp.status_code, 400)
    
    def test_registration_with_incorrect_email(self):
        request_data = self.methods.create_json_request(username='username1', password='abc12345',
                                        email='asd@mailcom', last_name="Smith", first_name="John")
        resp = self.client.post(self.registration_url, request_data,
             content_type="application/json")
        self.assertEqual(resp.status_code, 400)

    
    def test_registration_with_incorrect_email_and_password(self):
        request_data = self.methods.create_json_request(username='username1', password='ab234',
                                     email='asdmail.com', last_name="Smith", first_name="John")
        resp = self.client.post(self.registration_url, request_data,
             content_type="application/json")
        self.assertEqual(resp.status_code, 400)

    def test_registration_with_empty_email_and_password(self):
        request_data = self.methods.create_json_request(username='username1', password='',
                                                 email='', last_name="Smith", first_name="John")
        resp = self.client.post(self.registration_url, request_data,
             content_type="application/json")
        self.assertEqual(resp.status_code, 400)

    def test_registration_wih_no_password(self):
        request_data = self.methods.create_json_request(username='username1',
                                    email='asd@mail.com', last_name="Smith", first_name="John")
        resp = self.client.post(self.registration_url, request_data,
             content_type="application/json")
        self.assertEqual(resp.status_code, 400)

    def test_registration_with_no_email(self):
        request_data = self.methods.create_json_request(username='username1', password='abc1234')
        resp = self.client.post(self.registration_url, request_data,
             content_type="application/json")
        self.assertEqual(resp.status_code, 400)

    def test_registration_username_exists(self):
        request_data = self.methods.create_json_request(username='username1', password='abc12345',
                                        email='asd@mail.com', last_name="Smith", first_name="John")
        resp = self.client.post(self.registration_url, request_data,
             content_type="application/json")

        request_data = self.methods.create_json_request(username='username1', password='abc12345',
                                    email='asd@mail.com', last_name="Smith", first_name="John")
        resp = self.client.post(self.registration_url, request_data,
             content_type="application/json")
        self.assertEqual(resp.status_code, 460)


    def test_registration_with_correct_data_then_existing_username_and_email_correct_data(self):
        request_data = self.methods.create_json_request(username='username1', password='abc12345',
                                        email='asd@mail.com', first_name='Smith', last_name='John')
        resp1 = self.client.post(self.registration_url, request_data,
             content_type="application/json")

        request_data = self.methods.create_json_request(username='username1', password='abc12345',
                                    email='asacsd@mail.com', first_name='Smith', last_name='John')
        resp2 = self.client.post(self.registration_url, request_data,
             content_type="application/json")

        request_data = self.methods.create_json_request(username='username2', password='abc12345',
                                        email='asd@mail.com', first_name='Smith', last_name='John')
        resp3 = self.client.post(self.registration_url, request_data,
             content_type="application/json")

        request_data = self.methods.create_json_request(username='username2', password='abc12345',
                                        email='asascd@mail.com', first_name='Smith', last_name='John')
        resp4 = self.client.post(self.registration_url, request_data,
             content_type="application/json")
        self.assertEqual(resp1.status_code, 201)
        self.assertEqual(resp2.status_code, 460)
        self.assertEqual(resp3.status_code, 460)
        self.assertEqual(resp4.status_code, 201)
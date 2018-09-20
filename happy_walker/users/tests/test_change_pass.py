from django.test import TestCase, Client
from django.urls import reverse
import json
import mock
from .methods_for_test import MethodsForTest

class PasswordChangeTest(TestCase):

    def setUpTestData(self):
        self.registration_url = reverse('register')
        self.confirm_email_url = reverse('confirm_email')
        self.login_url = reverse('login')
        self.pass_change_url = reverse('change_password')

    def setUp(self):
        self.client = Client()
        print("-.-.-.-.-.-.-{}-.-.-.-.-.-.-.".format(self._testMethodName))

    methods = MethodsForTest()

    @mock.patch("users.tokens.TokenGenerator.check_token", methods.fake_check_token)
    def test_password_change_api_with_correct_data_input(self):
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
        login_data = self.methods.create_json_request(username_or_email='username1',
                             password='abc12345')
        resp3 = self.client.post(self.login_url, login_data,
                                 content_type="application/json")
        self.assertEqual(resp3.status_code, 230)
        change_pass_data = self.methods.create_json_request(old_password='abc12345', 
                  new_password="12345678", repeat_password="12345678")
        resp_from_change = self.client.post(self.pass_change_url, change_pass_data,
                                   content_type="application/json")
        self.assertEqual(resp_from_change.status_code, 201)

    @mock.patch("users.tokens.TokenGenerator.check_token", methods.fake_check_token)
    def test_change_password_with_no_password(self):
        
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
        login_data = self.methods.create_json_request(username_or_email='username1',
                             password='abc12345')
        resp3 = self.client.post(self.login_url, login_data,
                                 content_type="application/json")
        self.assertEqual(resp3.status_code, 230)
        change_pass_data = self.methods.create_json_request(new_password="12345678", 
                                                 repeat_password="12345678")
        resp_from_change = self.client.post(self.pass_change_url, change_pass_data,
                                   content_type="application/json")
        self.assertEqual(resp_from_change.status_code, 400)

    
    @mock.patch("users.tokens.TokenGenerator.check_token", methods.fake_check_token)
    def test_change_password_with_no_password(self):
        
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
        login_data = self.methods.create_json_request(username_or_email='username1',
                             password='abc12345')
        resp3 = self.client.post(self.login_url, login_data,
                                 content_type="application/json")
        self.assertEqual(resp3.status_code, 230)
        change_pass_data = self.methods.create_json_request()
        resp_from_change = self.client.post(self.pass_change_url, change_pass_data,
                                   content_type="application/json")
        self.assertEqual(resp_from_change.status_code, 400)

    @mock.patch("users.tokens.TokenGenerator.check_token", methods.fake_check_token)
    def test_change_password_with_wrong_password(self):
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
        login_data = self.methods.create_json_request(username_or_email='username1',
                             password='abc12345')
        resp3 = self.client.post(self.login_url, login_data,
                                 content_type="application/json")
        self.assertEqual(resp3.status_code, 230)
        change_pass_data = self.methods.create_json_request(old_password='wrongpass', 
                  new_password="12345678", repeat_password="12345678")
        resp_from_change = self.client.post(self.pass_change_url, change_pass_data,
                                   content_type="application/json")
        self.assertEqual(resp_from_change.status_code, 401)
        
    @mock.patch("users.tokens.TokenGenerator.check_token", methods.fake_check_token)
    def test_change_password_with_no_repeat_pass(self):
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
        login_data = self.methods.create_json_request(username_or_email='username1',
                             password='abc12345')
        resp3 = self.client.post(self.login_url, login_data,
                                 content_type="application/json")
        self.assertEqual(resp3.status_code, 230)
        change_pass_data = self.methods.create_json_request(old_password='abc12345', 
                  new_password="12345678")
        resp_from_change = self.client.post(self.pass_change_url, change_pass_data,
                                   content_type="application/json")
        self.assertEqual(resp_from_change.status_code, 400)

    
    @mock.patch("users.tokens.TokenGenerator.check_token", methods.fake_check_token)
    def test_password_change_api_with_unmatching_passwords(self):
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
        login_data = self.methods.create_json_request(username_or_email='username1',
                             password='abc12345')
        resp3 = self.client.post(self.login_url, login_data,
                                 content_type="application/json")
        self.assertEqual(resp3.status_code, 230)
        change_pass_data = self.methods.create_json_request(old_password='abc12345', 
                  new_password="12345678", repeat_password='notmatched')
        resp_from_change = self.client.post(self.pass_change_url, change_pass_data,
                                   content_type="application/json")        
        self.assertEqual(resp_from_change.status_code, 444)
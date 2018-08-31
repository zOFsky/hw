from django.test import TestCase, RequestFactory, Client
from django.urls import reverse
import json
import mock


class UpdateTest(TestCase):

    def setUp(self):
        self.registration_url = reverse('register')
        self.confirm_email = reverse('confirm_email')
        self.client = Client()
        print("----------{}-----------".format(self._testMethodName))

    def create_user(self, username, password, email,
                            first_name, last_name):
        my_dict = {
            "username": username,
            "password": password,
            "email": email,
            "first_name": first_name,
            "last_name": last_name,
        }
        json_string = json.dumps(my_dict)
        return json_string

    def create_email(self, id, token):

        my_dict = {
            "uid": id,
            "token": token,
        }
        json_string = json.dumps(my_dict)
        return json_string

    def fake_check_token(self, user, token):
        if token == 'true':
            return True
        else:
            return False

    @mock.patch("users.tokens.TokenGenerator.check_token", fake_check_token)

    def test_confirm_email_api_with_correct_data_input(self):
        user = self.create_user('username1', 'abc1234', 'asd@mail.com',
                                                'name', 'lastname')
        resp = self.client.post(self.registration_url, user,
             content_type="application/json")
        self.assertEqual(resp.status_code, 201)
        resp = json.loads(resp.content)
        email = self.create_email(str(resp['uid']), 'true')
        resp2 = self.client.post(self.confirm_email, email,
                                content_type="application/json")
        self.assertEqual(resp2.status_code, 200)

    def test_confirm_email_api_with_invalid_token(self):
        user = self.create_user('username1', 'abc1234', 'asd@mail.com',
                                                'name', 'lastname')
        resp = self.client.post(self.registration_url, user,
             content_type="application/json")
        self.assertEqual(resp.status_code, 201)
        resp = json.loads(resp.content)
        email = self.create_email(str(resp['uid']), 'false')
        resp2 = self.client.post(self.confirm_email, email,
                                content_type="application/json")
        self.assertEqual(resp2.status_code, 400)

    def test_confirm_email_api_with_invalid_user_id(self):
        user = self.create_user('username1', 'abc1234', 'asd@mail.com',
                                                'name', 'lastname')
        resp = self.client.post(self.registration_url, user,
             content_type="application/json")
        self.assertEqual(resp.status_code, 201)
        resp = json.loads(resp.content)
        email = self.create_email('1782', 'true')
        resp2 = self.client.post(self.confirm_email, email,
                                content_type="application/json")
        self.assertEqual(resp2.status_code, 400)
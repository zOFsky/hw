from django.test import TestCase, Client
from django.urls import reverse
import json
import mock


class UpdateTest(TestCase):

    def setUp(self):
        self.registration_url = reverse('register')
        self.confirm_email_url = reverse('confirm_email')
        self.login_url = reverse('login')
        self.client = Client()
        print("----------{}-----------".format(self._testMethodName))

    def get_profile_url(self, args):
        return reverse('profile', args=[args])

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
    def test_get_profile_with_correct_data_input(self):
        request_data = self.create_json_request(username='username1', password='abc1234',
                                                email='asd@mail.com', first_name='r', last_name='r')
        resp = self.client.post(self.registration_url, request_data,
                                content_type="application/json")
        self.assertEqual(resp.status_code, 201)
        resp = json.loads(resp.content)
        email = self.create_email(str(resp['uid']), 'true')
        resp_confirm_email = self.client.post(self.confirm_email_url, email,
                                              content_type="application/json")
        self.assertEqual(resp_confirm_email.status_code, 200)
        resp3 = self.client.get(self.get_profile_url('me'))
        self.assertEqual(resp3.status_code, 200)


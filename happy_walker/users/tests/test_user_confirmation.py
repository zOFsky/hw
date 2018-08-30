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

    def create_user(self, username="", password="", email="",
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
            "id": id,
            "token": token,
        }
        json_string = json.dumps(my_dict)
        return json_string

    def fake_send_email(self, email, mail_subject, text_email, html_email, context):


    @mock.patch("users.email_sender.EmailSender.send_email", fake_send_email)

    def test_confirm_email_api_with_correct_data_input(self):
        user = self.create_user('username1', 'abc1234', 'asd@mail.com',
                                                'name', 'lastname')
        resp = self.client.post(self.registration_url, user,
             content_type="application/json")
        self.assertEqual(resp.status_code, 201)

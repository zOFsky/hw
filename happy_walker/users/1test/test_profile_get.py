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

    def setUp(self):
        self.client = Client()
        print("----------{}-----------".format(self._testMethodName))

    methods = MethodsForTest()

    @mock.patch("users.tokens.TokenGenerator.check_token", methods.fake_check_token)
    def test_get_profile_with_correct_data_input(self):
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
        resp3 = self.client.get(self.methods.get_profile_url('me'))
        self.assertEqual(resp3.status_code, 200)

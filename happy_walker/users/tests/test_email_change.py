from django.test import TestCase, RequestFactory, Client
from django.urls import reverse, resolve
import json

class UpdateTest(TestCase):

  
    def setUp(self):
        self.registration_url = reverse('register')
        self.login_url = reverse('login')
        self.update_url = reverse('profile', args=['me'])
        self.change_email_url = reverse('change_email')
        self.client = Client()
        print("-+-+-+-+-+-+-+-+-+-{}-+-+-+-+-+-+-+-+-+-+-".format(self._testMethodName))

    def create_json_request(self, username="", password="", email="",
                    first_name="", last_name="", username_or_email="", uid="", token="", 
                    new_email=""):
        my_dict = {
            "username": username,
            "password": password,
            "email": email,
            "first_name": first_name,
            "last_name": last_name,
            "username_or_email": username_or_email,
            "email": email,
            "token": token,
            "new_email": new_email,
            "uid": uid,
        }
        json_string = json.dumps(my_dict)
        return json_string

    
    
    def test_email_change_with_correct_email(self):
        request_data = self.create_json_request(username='username1', password='abc1234', 
                                       email='asd@mail.com', last_name="Smith", first_name="John")
        resp = self.client.post(self.registration_url, request_data,
             content_type="application/json")
        self.assertEqual(resp.status_code, 201)
        login_data = self.create_json_request(username_or_email='username1',
                             password='abc1234')
        resp2 = self.client.post(self.login_url, login_data, 
                                 content_type="application/json")
        self.assertEqual(resp2.status_code, 230)
        update_data = self.create_json_request(first_name="Jane", email="asd@fun.com", last_name="Doe")
        resp3 = self.client.post(self.update_url,update_data,
                                 content_type="application/json")
        self.assertEqual(resp3.status_code, 202)
        token_data = json.loads(resp3.content)
        change_mail_data = self.create_json_request(token=token_data["token"],
                                  uid=token_data["uid"],new_email="new@mail.com")
        resp_email_changer = self.client.post(self.change_email_url, change_mail_data,
                                 content_type="application/json")

        self.assertEqual(resp_email_changer.status_code, 201) 

    def test_email_change_with_correct_email2(self):
        request_data = self.create_json_request(username='username1', password='abc1234', 
                                       email='asd@mail.com', last_name="Smith", first_name="John")
        resp = self.client.post(self.registration_url, request_data,
             content_type="application/json")
        self.assertEqual(resp.status_code, 201)
        login_data = self.create_json_request(username_or_email='username1',
                             password='abc1234')
        resp2 = self.client.post(self.login_url, login_data, 
                                 content_type="application/json")
        self.assertEqual(resp2.status_code, 230)
        update_data = self.create_json_request(first_name="Andriy", email="asd@fun.com", last_name="Doe")
        resp3 = self.client.post(self.update_url,update_data,
                                 content_type="application/json")
        self.assertEqual(resp3.status_code, 202)
        token_data = json.loads(resp3.content)
        change_mail_data = self.create_json_request(token=token_data["token"],
                                  uid=token_data["uid"],new_email="new@mailcom")
        resp_email_changer = self.client.post(self.change_email_url, change_mail_data,
                                 content_type="application/json")

        self.assertEqual(resp_email_changer.status_code, 401) 

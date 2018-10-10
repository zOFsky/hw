from django.urls import reverse
import json

class MethodsForTest:

    def get_profile_url(self, args):
        return reverse('profile', args=[args])

    def fake_check_token(self, user, token):
        if token == 'true':
            return True
        else:
            return False

    def create_json_request(self, **kwargs):
        my_dict = {}

        for key, value in kwargs.items():
            my_dict[key] = value

        json_string = json.dumps(my_dict)
        return json_string
import time, datetime
from django.contrib.auth.models import User
from django.conf import settings
from users.models import Profile, Location
from django.http import HttpResponse, HttpRequest, JsonResponse
from django.http import HttpResponseRedirect, HttpResponseBadRequest
from django.template.loader import get_template
from django.views.generic import View
from django.contrib.auth import authenticate, login, logout
from django.db.models import Q, Avg, Sum
from oauthlib.oauth2.rfc6749.errors import MissingCodeError
from django.core.exceptions import ObjectDoesNotExist
from google_auth_oauthlib.flow import Flow
import googleapiclient.discovery
import json
from .custom_validator import CustomValidator
from .tokens import TokenGenerator
from .email_sender import EmailSender
#from . import epochtime
import time
import calendar
from random import choice
from string import ascii_uppercase
import cloudinary


class UserRegisterView(View):
       
    validation_schema = {
        'password': {
            'required': True,
            'type': 'string',
            'minlength': 8,
            'empty': False
            },
        'email': {
            'required': True,
            'type': 'string', 
            'regex': '^[a-zA-Z0-9_.+-]+@[a-zA-Z0-9-]+\.[a-zA-Z0-9-.]+$',
            'empty': False
            },
        'username': {
            'required': True,
            'type': 'string',
            'regex': '^[\w]+$',
            'minlength': 2,
            'maxlength': 30,
            'empty': False,
        },
        'first_name': {
            'required': True,
            'type': 'string',
            'minlength': 2,
            'maxlength': 30,
            'regex': '^[a-zA-Z]+$',
            'empty': False,
        },
        
        'last_name': {
            'required': True,
            'type': 'string',
            'minlength': 2,
            'maxlength': 30,
            'regex': '^[a-zA-Z]+$',
            'empty': False,
        },
        'location': {
            'required': True,
            'empty': False,
            'type': 'dict',
            'schema': {
                'city': {
                    'required': True,
                    'type': 'string',
                    'empty': False
                },
                'lat': {
                    'required': True,
                    'type': 'number',
                    'empty': False
                },
                'lng': {
                    'required': True,
                    'type': 'number',
                    'empty': False
                }
            }
        }

    }
    
    def post(self, request):
        # input validation
        # if data does not pass validation we send response with errors
        validator = CustomValidator(self.validation_schema)
        if validator.request_validation(request):
            errors_dict = validator.request_validation(request)
            return JsonResponse(errors_dict, status=400)
        else:
            data = json.loads(request.body)
        # check if username or email already exists in our database
        if not(User.objects.filter(
             Q(username=data['username']) |
             Q(email=data['email'])
             ).exists()):
            # if user doesn't exist we create him with data
            User.objects.create_user(username=data['username'], email=data['email'], password=data['password'],
                                     first_name=data['first_name'], last_name=data['last_name'], is_active=False)

            user = User.objects.get(username=data['username'])
            profile = Profile.objects.get(user_id=user.id)
            profile.location = Location(lat=data['location']['lat'], lng=data['location']['lng'],
                                        city=data['location']['city'])
            profile.save()

            # send email
            token_generator = TokenGenerator()
            confirmation_email = EmailSender()
            context = {
                'uid': user.id,
                'token': token_generator.make_token(user),
            }
            email = user.email
            mail_subject = 'Activate your HappyWalker account'
            html_email = get_template('acc_active_email.html')
            text_email = get_template('acc_active_email')
            confirmation_email.send_email(email, mail_subject, text_email, html_email, context)

            return JsonResponse({
                "uid": user.id,
                "message": "user successfully created",
                }, status=201)
        # in case username or email already exists in database we return that message
        else:
            return JsonResponse({
                "errors": [{"message": "user with that credentials already exists",
                            "code": "registration.user_exists"}]
                }, status=460)


class ConfirmEmailView(View):

    validation_schema = {
        'uid': {
            'required': True,
            'type': 'integer',
            'empty': False
        },
        'token': {
            'required': True,
            'type': 'string',
            'empty': False
        },
    }

    def post(self, request):
        validator = CustomValidator(self.validation_schema)
        if validator.request_validation(request):
            errors_dict = validator.request_validation(request)
            return JsonResponse(errors_dict, status=400)
        else:
            data = json.loads(request.body)

        uid = data['uid']
        token = data['token']
        try:
            user = User.objects.get(id=uid)
        except ObjectDoesNotExist:
            return JsonResponse({
                "errors": [{
                    "message": "This user does not exist",
                    "code": "ObjectDoesNotExist",
                    "field": "uid"
                }]
            }, status=400)
        token_generator = TokenGenerator()
        if token_generator.check_token(user, token):
            User.objects.filter(id=uid).update(is_active='True')
            login(request, user)
            return JsonResponse({
                "message": "user successfully activated"
            }, status=200)
        else:
            return JsonResponse({
                "errors": [{
                    "message": "Activation link is invalid",
                    "code": "token.invalid",
                    "field": "token"
                }]
            }, status=400)


class ResendEmailView(View):

    def get(self, request, user_id):

        user = User.objects.get(id=user_id)

        token_generator = TokenGenerator()
        confirmation_email = EmailSender()
        context = {
            'uid': user.id,
            'token': token_generator.make_token(user),
        }
        email = user.email
        mail_subject = 'Activate your HappyWalker account'
        html_email = get_template('acc_active_email.html')
        text_email = get_template('acc_active_email')
        confirmation_email.send_email(email, mail_subject, text_email, html_email, context)

        return JsonResponse({
            "uid": user.id,
            "message": "Success",
        }, status=201)


class ChangeEmailView(View):

    validation_schema = {
        'uid': {
            'required': True,
            'type': 'integer',
            'empty': False
        },
        'token': {
            'required': True,
            'type': 'string',
            'empty': False
        },
        'new_email': {
            'required': True,
            'type': 'string',
            'regex': '^[a-zA-Z0-9_.+-]+@[a-zA-Z0-9-]+\.[a-zA-Z0-9-.]+$',

        }
    }

    def post(self, request):
        validator = CustomValidator(self.validation_schema)
        if validator.request_validation(request):
            errors_dict = validator.request_validation(request)
            return JsonResponse(errors_dict, status=400)
        else:
            data = json.loads(request.body)

        uid = data['uid']
        token = data['token']
        new_email = data['new_email']
        try:
            user = User.objects.get(id=uid)
        except ObjectDoesNotExist:
            return JsonResponse({
                "message": "This user does not exist",
            }, status=401)
        token_generator = TokenGenerator()
        if token_generator.check_token(user, token):
            User.objects.filter(id=uid).update(email=new_email)
            return JsonResponse({
                "id": uid,
                "new_email": new_email,
                "message": "email successfully updated"
            }, status=201)
        else:
            return HttpResponseBadRequest({
                "message": "activation link is invalid"
            }, status=406)


class UserLoginView(View):
    validation_schema = {
        'password': {
            'required': True,
            'type': 'string', 
            'empty': False
            },
        'username_or_email': {
            'required': True,
            'type': 'string', 
            'empty': False
            },
    }

    def post(self, request):
        # data validation
        validator = CustomValidator(self.validation_schema)
        if validator.request_validation(request):
            errors_dict = validator.request_validation(request)
            return JsonResponse(errors_dict, status=400)
        else:
            data = json.loads(request.body)
        # try to find user in our database
        try:
            existing_user = User.objects.filter(Q(username=data['username_or_email']) |
                                                Q(email=data['username_or_email'])).get()
        # return response with error if we couldn't find user with entered data
        except ObjectDoesNotExist:
            return JsonResponse({
                "errors": [{"message": "user does not exist in our database",
                            "code": "login.user_does_not_exists"}]
                }, status=432)
        # checking if user is active
        # at this point user is always active, but it will be changed in further development
        if not existing_user and not existing_user.is_active:
            return JsonResponse({
                "errors": [{"message": "user is not active",
                            "code": "login.user_is_not_active"}]
                }, status=455)
        # if user is active we authenticate him and log him in
        elif existing_user:
            user = authenticate(username=existing_user.username, 
                                password=data['password'])
            if user is not None:

                profile = Profile.objects.get(user_id=existing_user.id)
                if not profile.refresh_token:
                    return JsonResponse({
                        "message": "user did not give access",
                        "uid": existing_user.id
                    }, status=423)

                login(request, user)
                if not request.session.exists(request.session.session_key):
                    request.session.create() 
                return JsonResponse({
                    "message": "login successfull",
                    "token": request.session.session_key
                    }, status=230)
            # if user didn't pass authentication we send message
            else:
                return JsonResponse({
                    "errors": [{"message": "password incorrect",
                                "code": "login.incorrect_password"}]
                }, status=467)


class ProfileView(View):

    validation_schema = {
        'email': {
            'required': True,
            'type': 'string',
            'regex': '^[a-zA-Z0-9_.+-]+@[a-zA-Z0-9-]+\.[a-zA-Z0-9-.]+$',
        },
        'first_name': {
            'required': True,
            'type': 'string',
            'empty': False,
        },
        'last_name': {
            'required': True,
            'type': 'string',
            'empty': False,
        },
        'location': {
            'required': True,
            'empty': True,
            'type': 'dict',
            'schema': {
                'city': {
                    'type': 'string',
                    'empty': False
                },
                'lat': {
                    'type': 'number',
                    'empty': False
                },
                'lng': {
                    'type': 'number',
                    'empty': False
                }
            }
        }
    }

    def get(self, request, user_id):
        if user_id == 'me':
            user = User.objects.get(id=request.user.id)
        else:
            try:
                user = User.objects.get(id=user_id, is_active=True)
            except ObjectDoesNotExist:
                return JsonResponse({
                    "message": "This user does not exist",
                }, status=400)

        profile = {
            'username': user.username,
            'first_name': user.first_name,
            'last_name': user.last_name,
            'favorites': user.profile.favorites,
            'location': {
                'city': user.profile.location.city,
                'lat': user.profile.location.lat,
                'lng': user.profile.location.lng
            }
        }

        if user.profile.image.url:
            profile['image'] = user.profile.image.url
        else:
            profile['image'] = user.profile.google_image

        if user_id == str(request.user.id) or user_id == 'me':
            profile['email'] = user.email

        return JsonResponse(profile, status=200)

    def post(self, request, user_id):
        if user_id != 'me':
            return JsonResponse({
                "message": "user_id is not 'me', access denied"
            }, status=401)
        # input validation
        # if data does not pass validation we send response with errors

        validator = CustomValidator(self.validation_schema)
        if validator.request_validation(request):
            errors_dict = validator.request_validation(request)
            return JsonResponse(errors_dict, status=400)
        else:
            data = json.loads(request.body)
            user = User.objects.get(id=request.user.id)
            profile = Profile.objects.get(user_id=request.user.id)

            user.first_name = data["first_name"]
            user.last_name = data["last_name"]

            user.save()

            if data['location']:
                profile.location = Location(lat=data['location']['lat'], lng=data['location']['lng'],
                                            city=data['location']['city'])
                profile.save()
            else:
                profile.location = Location()
                profile.save()

            if data["email"] != user.email:
                # sending confirmation letter to new email
                token_generator = TokenGenerator()
                confirmation_email = EmailSender()
                context = {
                    'uid': user.id,
                    'token': token_generator.make_token(user),
                    'new_email': data["email"]
                }
                email = data['email']
                mail_subject = 'Email change confirmation'
                html_email = get_template('change_email.html')
                text_email = get_template('change_email')
                confirmation_email.send_email(email, mail_subject, text_email, html_email, context)

                return JsonResponse({
                    "message": "please confirm your new email"
                }, status=202)
            return JsonResponse({
                "message": "user successfully updated"
            }, status=201)


class FavoritesView(View):

    def get(self, request, favorite_id):
        profile = Profile.objects.get(user_id=request.user.id)
        favorite_id = int(favorite_id)

        if favorite_id in profile.favorites:
            profile.favorites.remove(favorite_id)
        else:
            profile.favorites.append(favorite_id)

        profile.save()

        return JsonResponse({
            "message": "Success",
            "favorites": profile.favorites
        }, status=200)


class UploadPhotoView(View):

    def post(self, request):
        if 'image' in request.FILES:
            if request.FILES['image'].size < 5242880:

                profile = Profile.objects.get(user_id=request.user.id)
                old_image = profile.image.public_id
                if old_image:
                    cloudinary.uploader.destroy(old_image)
                profile.image = request.FILES['image']
                profile.save()

                return JsonResponse({
                    "image": profile.image.url
                }, status=200)
            else:
                return JsonResponse({
                    "message": "File too large. Size should not exceed 5 MB",
                    "code": "size"
                }, status=400)
        else:
            return JsonResponse({
                "message": "file not uploaded",
                "code": "empty"
            }, status=400)


class UserLogoutView(View):
    def get(self, request):
        logout(request)
        return JsonResponse({
            "message": "succesfully logged out"
        }, status=200)


class ChangePasswordView(View):

    validation_schema = {
        'old_password': {
            'required': True,
            'type': 'string',
            'minlength': 8,
            'empty': False
            },
        'new_password': {
            'required': True,
            'type': 'string',
            'minlength': 8,
            'empty': False
            },
        'repeat_password': {
            'required': True,
            'type': 'string',
            'minlength': 8,
            'empty': False
            },
        }

    def post(self, request):
        validator = CustomValidator(self.validation_schema)
        if validator.request_validation(request):
            errors_dict = validator.request_validation(request)
            return JsonResponse(errors_dict, status=400)
        data = json.loads(request.body)
        current_user = request.user
        if not current_user.check_password(data['old_password']):
            return JsonResponse({"message": "password is incorrect"}, status=401)
        else:
            if data['new_password'] == data['repeat_password']:
                current_user.set_password(data['new_password'])
                current_user.save()
                return JsonResponse({"message": "password successfully updated"}, status=201)
            else:
                return JsonResponse({"message": "passwords doesn't match"}, status=444)


class ForgotPasswordView(View):
    validation_schema = {
        'email': {
            'required': True,
            'empty': False,
            'type': 'string',
            'regex': '^[a-zA-Z0-9_.+-]+@[a-zA-Z0-9-]+\.[a-zA-Z0-9-.]+$',
        },  
    }

    def post(self, request):
        validator = CustomValidator(self.validation_schema)
        if validator.request_validation(request):
            errors_dict = validator.request_validation(request)
            return JsonResponse(errors_dict, status=400)
        data = json.loads(request.body)
        try:
            user = User.objects.get(email=data['email'])
        except ObjectDoesNotExist:
            user = False
        if user:
            # send email
            token_generator = TokenGenerator()
            confirmation_email = EmailSender()
            context = {
                'uid': user.id,
                'token': token_generator.make_token(user),
            }
            email = data['email']
            mail_subject = 'Reset your password'
            html_email = get_template('reset_password.html')
            text_email = get_template('reset_password')
            confirmation_email.send_email(email, mail_subject, text_email, html_email, context)
            return JsonResponse({
                'message': 'Check your email to change your password'
            }, status=202)
        else:
            return JsonResponse({
                'message': 'Check your email to change your password'
            }, status=200)


class ResetPasswordView(View):

    validation_schema = {
        'uid': {
            'required': True,
            'type': 'integer',
            'empty': False
        },
        'token': {
            'required': True,
            'type': 'string',
            'empty': False
        },
        'password': {
            'required': True,
            'type': 'string',
            'minlength': 8,
            'empty': False
            },
        'repeat_password': {
            'required': True,
            'type': 'string',
            'minlength': 8,
            'empty': False
            },
    }

    def post(self, request):
        validator = CustomValidator(self.validation_schema)
        if validator.request_validation(request):
            errors_dict = validator.request_validation(request)
            return JsonResponse(errors_dict, status=400)
        else:
            data = json.loads(request.body)

        uid = data['uid']
        token = data['token']
        if data['password'] == data["repeat_password"]:
            try:
                user = User.objects.get(id=uid)
            except ObjectDoesNotExist:
                return JsonResponse({
                    "message": "This user does not exist",
                }, status=404)
            token_generator = TokenGenerator()
            if token_generator.check_token(user, token):
                user.set_password(data['password'])
                user.save()
                return JsonResponse({
                    "id": uid,
                    "message": "password successfully updated"
                }, status=201)
            else:
                return JsonResponse({
                    "message": "activation link is invalid"
                }, status=406)
        else:
            return JsonResponse({
                    "message":"passwords doesn't match"
                }, status=444)


class OAuthView(View):

    validation_schema = {
        'code': {
            'required': True,
            'type': 'string',
            'empty': False
        }
    }

    def post(self, request):

        validator = CustomValidator(self.validation_schema)
        if validator.request_validation(request):
            errors_dict = validator.request_validation(request)
            return JsonResponse(errors_dict, status=400)
        else:
            data = json.loads(request.body)

        flow = Flow.from_client_secrets_file(
            settings.CLIENT_SECRETS_FILE,
            scopes=None,
            redirect_uri=settings.REDIRECT_URI)

        try:
            flow.fetch_token(code=data['code'])
        except:
            return JsonResponse({'message': 'Bad request'}, status=401)

        credentials = flow.credentials

        google_user = googleapiclient.discovery.build(
            'plus', 'v1', credentials=credentials)
        google_user = google_user.people().get(userId='me').execute()
        google_id = google_user['id']

        if Profile.objects.filter(google_id=google_id).exists():
            profile = Profile.objects.get(google_id=google_id)

            login(request, profile.user)
            return JsonResponse({
                "message": "login success",
            }, status=200)
        else:

            first_name = google_user['name']['givenName']
            last_name = google_user['name']['familyName']
            image = google_user['image']['url']
            email = google_user['emails'][0]['value']
            nickname = "{}{}".format(first_name, calendar.timegm(time.gmtime()))
            password = ''.join(choice(ascii_uppercase) for i in range(12))
            user = User.objects.create_user(username=nickname, email=email, password=password,
                                            first_name=first_name, last_name=last_name, is_active=True)
            Profile.objects.filter(user_id=user.id).update(access_token=credentials.token,
                                                           refresh_token=credentials.refresh_token,
                                                           google_image=image, google_id=google_id)

        login(request, user)

        return JsonResponse({
            "message": "login success",
        }, status=200)


class CredentialsView(View):

    validation_schema = {
        'code': {
            'required': True,
            'type': 'string',
            'empty': False
        },
        'uid': {
            'required': True,
            'type': 'integer',
            'empty': False
        }
    }

    def post(self, request):

        validator = CustomValidator(self.validation_schema)
        if validator.request_validation(request):
            errors_dict = validator.request_validation(request)
            return JsonResponse(errors_dict, status=400)
        else:
            data = json.loads(request.body)

        flow = Flow.from_client_secrets_file(
            settings.CLIENT_SECRETS_FILE,
            scopes=None,
            redirect_uri=settings.REDIRECT_URI)

        try:
            flow.fetch_token(code=data['code'])
        except:
            return JsonResponse({'message': 'Bad request'}, status=401)

        credentials = flow.credentials

        google_user = googleapiclient.discovery.build(
            'plus', 'v1', credentials=credentials)
        google_user = google_user.people().get(userId='me').execute()
        google_id = google_user['id']

        if Profile.objects.filter(google_id=google_id).exists():
            return JsonResponse({
                "message": "this account is already in use",
                "uid": data['uid']
            }, status=401)
        else:
            Profile.objects.filter(user_id=data['uid']).update(access_token=credentials.token,
                                                               refresh_token=credentials.refresh_token,
                                                               google_id=google_id)
            user = User.objects.get(id=data['uid'])
            login(request, user)

        return JsonResponse({"message": "login success"}, status=200)


class TopWalkersView(View):

    def get(self, request):

        user = User.objects.get(id=request.user.id)

        if user.profile.location.city == '':
            return JsonResponse({'top_walkers': []}, status=200)

        lat = user.profile.location.lat
        lng = user.profile.location.lng

        top_walkers = []
        data = Profile.objects.filter(location={'lat': lat, 'lng': lng})
        data = data[::1]
        for walker in data:
            dict = {}
            if walker.image.url:
                dict['image'] = walker.image.url
            else:
                dict['image'] = walker.google_image
            dict['id'] = walker.user_id
            dict['first_name'] = walker.user.first_name
            dict['last_name'] = walker.user.last_name
            top_walkers.append(dict)

        return JsonResponse({'top_walkers': top_walkers}, status=200)

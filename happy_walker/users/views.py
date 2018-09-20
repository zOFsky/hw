from django.contrib.auth.models import User
from users.models import Profile
from django.http import HttpResponse, HttpRequest, JsonResponse
from django.http import HttpResponseRedirect, HttpResponseBadRequest
from django.template.loader import get_template
from django.views.generic import View
from django.contrib.auth import authenticate, login
from django.db.models import Q
from django.core.exceptions import ObjectDoesNotExist
import json
from .custom_validator import CustomValidator
from .tokens import TokenGenerator
from .email_sender import EmailSender


class UserRegisterView(View):
       
    validation_schema = {
        'password': {
            'required': True,
            'type': 'string',
            'minlength': 6,
            'empty': False
            },
        'email': {
            'required': True,
            'type': 'string', 
            'regex': '^[a-zA-Z0-9_.+-]+@[a-zA-Z0-9-]+\.[a-zA-Z0-9-.]+$',
            'empty': False
            },
        'username':{
            'required': True,
            'type': 'string',
            'regex': '^[\w]+$',
            'minlength': 2,
            'maxlength': 30,
            'empty': False,
        },
        'first_name':{
            'required': True,
            'type': 'string',
            'minlength': 2,
            'maxlength': 30,
            'regex': '^[a-zA-Z]+$',
            'empty': False,
        },
        
        'last_name':{
            'required': True,
            'type': 'string',
            'minlength': 2,
            'maxlength': 30,
            'regex': '^[a-zA-Z]+$',
            'empty': False,
        }

    }
    
    def post(self, request):
        #input validation 
        #if data does not pass validation we send response with errors
        validator = CustomValidator(self.validation_schema)
        if validator.request_validation(request):
            errors_dict = validator.request_validation(request)
            return JsonResponse(errors_dict, status = 400)
        else:
            data = json.loads(request.body)
        #check if username or email already exists in our database
        if not(User.objects.filter(
             Q(username=data['username']) |
             Q(email=data['email'])
             ).exists()):
            #if user doesn't exist we create him with data
            User.objects.create_user(username=data['username'], email=data['email'],
                password=data['password'], first_name=data['first_name'],
                last_name=data['last_name'], is_active=False)

            # send email
            user = User.objects.get(username=data['username'])
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
                "message" : "user successfully created",
                }, status=201)
        # in case username or email already exists in database we return that message
        else:
            return JsonResponse({
                "errors":[{"message" : "user with that credentials already exists",
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
                "message": "This user does not exist",
            }, status=400)
        token_generator = TokenGenerator()
        if token_generator.check_token(user, token):
            User.objects.filter(id=uid).update(is_active='True')
            login(request, user)
            return JsonResponse({
                "id": uid,
                "message": "user successfully activated"
            }, status=200)
        else:
            return JsonResponse({
                "message": "activation link is invalid"
            }, status=400)


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
            return JsonResponse(errors_dict, status=401)
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
            }, status=400)
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
        #data validation
        validator = CustomValidator(self.validation_schema)
        if validator.request_validation(request):
            errors_dict = validator.request_validation(request)
            return JsonResponse(errors_dict, status = 400)
        else:
            data = json.loads(request.body)
        #try to find user in our database
        try:
            existing_user = User.objects.filter(Q(username=data['username_or_email']) |
                                          Q(email=data['username_or_email'])).get()
        #return response with error if we couldn't find user with entered data
        except:
            return JsonResponse({
                "errors":[{"message" : "user does not exist in our database",
                "code": "login.user_does_not_exists"}]
                }, status=432)
        #checking if user is active
        #at this point user is always active, but it will be changed in further development 
        if existing_user and existing_user.is_active==False:
            return JsonResponse({
                "errors":[{"message" : "user is not active",
                "code": "login.user_is_not_active"}]
                }, status=455)
        #if user is active we authenticate him and log him in   
        elif existing_user:
            user = authenticate(username=existing_user.username, 
                                             password=data['password'])
            if user is not None:
                login(request, user)
                if not request.session.exists(request.session.session_key):
                    request.session.create() 
                return JsonResponse({
                    "message": "login successfull",
                    "token": request.session.session_key
                    }, status=230)
            #if user didn't pass authentication we send message
            else:
                return JsonResponse({
                "errors":[{"message" : "password incorrect",
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
        # 'gender': {
        #     'required': True,
        #     'type': 'string',
        #     'empty': True,
        # },
        # 'age': {
        #     'required': True,
        #     'type': 'integer',
        #     'empty': True,
        # },
        # 'weight': {
        #     'required': True,
        #     'type': 'integer',
        #     'empty': True,
        # }
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
            'last_name': user.last_name
        }

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
            profile.age = data['age']
            profile.weight = data['weight']
            profile.gender = data['gender']

            user.save()
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


class Image(View):

    def post(self, request):
        profile = Profile.objects.get(user_id=request.user.id)
        profile.image = request.FILES['image']
        profile.save()
        profile = Profile.objects.get(user_id=request.user.id)

        return JsonResponse({
            "image": profile.image.url
        }, status=200)

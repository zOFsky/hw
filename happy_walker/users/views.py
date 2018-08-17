from django import forms
from django.contrib.auth.models import User
from django.http import HttpResponse, HttpRequest, JsonResponse
from django.http import HttpResponseRedirect, HttpResponseBadRequest
from django.shortcuts import render
from django.views.generic import View
from cerberus import Validator
from django.contrib.auth import authenticate, login
from django.db.models import Q
import json
from . import custom_validator as cv

class ValidationView(View):
    validation_schema = {}

    def request_validation(self, request):
        if len(request.body) > 0 and len(request.FILES) == 0:
            data = json.loads(request.body)

        data_validator = Validator(self.validation_schema, 
                                   error_handler=cv.CustomErrorHandler)
        data_validator.allow_unknown = True
        # Validating password and email using cerberus library
        # validation schema is coded in validation.py file
        data_validator(data)
        errors_dict = {}
        if data_validator.errors:
            print("ERRORS: {}".format(data_validator.errors))
            errors_dict = {
                'errors': []
            }

            for key, value in data_validator.errors.items():
                for index in range(len(data_validator.document_error_tree[key].errors)):
                    errors_dict['errors'].append({
                        "field": key,
                        "code": data_validator.document_error_tree[key].errors[index].rule,
                        "message": value[index]
                    })
                    
        return errors_dict

class UserRegister(ValidationView):
       
    validation_schema = {
        'password': {
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
    }
    
    def post(self, request):
        #input validation 
        #if data does not pass validation we send response with errors
        if self.request_validation(request):
            errors_dict = self.request_validation(request)
            return JsonResponse(errors_dict, status = 400)
        else:
            data = json.loads(request.body)
        #check if username or email already exists in our database
        if not(User.objects.filter(
             Q(username=data['username']) |
             Q(email=data['email'])
             ).exists()):
            #if user doesn't exist we create him with data
            User.objects.create_user(username=data['username'],email=data['email'], 
                password=data['password'], first_name=data['firstname'],
                last_name=data['lastname'])
            return JsonResponse({
                "message" : "user successfully created"
                }, status=201)
        # in case username or email already exists in database we return that message
        else:
            return HttpResponseBadRequest({
                "errors":[{"message" : "user with that credentials already exists",
                "code": "registration.user_exists"}]
                }, status=460)


class UserLogin(ValidationView):
    validation_schema = {
        'password': {
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
        if self.request_validation(request):
            errors_dict = self.request_validation(request)
            return JsonResponse(errors_dict, status = 400)
        else:
            data = json.loads(request.body)
        #try to find user in our database
        try:
            existing_user = User.objects.filter(Q(username=data['username_or_email']) |
                                          Q(email=data['username_or_email'])).get()
        #return response with error if we couldn't find user with entered data
        except:
            return HttpResponseBadRequest({
                "errors":[{"message" : "user does not exist in our database",
                "code": "login.user_does_not_exists"}]
                }, status=432)
        #checking if user is active
        #at this point user is always active, but it will be changed in further development 
        if existing_user and existing_user.is_active==False:
            return HttpResponseBadRequest({
                "errors":[{"message" : "user is not active",
                "code": "login.user_is_not_active"}]
                }, status=455)
        #if user is active we authenticate him and log him in   
        elif existing_user:
            user = authenticate(username=existing_user.username, 
                                             password=data['password'])
            if user is not None:
                login(request, user)
                return JsonResponse({
                    "message": "login successfull",
                    "token": request.session.session_key
                    }, status=230)
            #if user didn't pass authentication we send message
            else:
                return HttpResponseBadRequest({
                "errors":[{"message" : "password incorrect",
                "code": "login.incorrect_password"}]
                }, status=467)

class UserUpdateProfile(View):
    validation_schema = {
            'email': {
            'type': 'string', 
            'regex': '^[a-zA-Z0-9_.+-]+@[a-zA-Z0-9-]+\.[a-zA-Z0-9-.]+$',
            'empty': False
            },
    }
    def put(self, request, user_id):
        
        #input validation 
        #if data does not pass validation we send response with errors
        if self.request_validation(request):
            errors_dict = self.request_validation(request)
            return JsonResponse(errors_dict, status = 400)
        else:
            data = json.loads(request.body)
        #check if user trying to update his own profile
        current_user_id = data['user_id']
        if (current_user_id != user_id) || (user_id != 'me'):
            return JsonResponse({"message": "Access Denied!"}, status=403)
        else:
            user = User.objects.filter(id=user_id).get()
            if data["first_name"]:
                user.first_name = data["first_name"]
            if data["last_name"]:
                user.last_name = data["last_name"]
            if data["username"]:
                #TODO: unique check
                user.username = data["username"]
            if data["email"]:
                #TODO: confirmation send
                user.email = data["email"]
            user.save()
            return JsonResponse({
                "message" : "user successfully updated"
                }, status=201)
        # in case username or email already exists in database we return that message
        

from django import forms
from django.contrib.auth.models import User
from django.http import HttpResponse, HttpRequest, JsonResponse
from django.http import HttpResponseRedirect, HttpResponseBadRequest
from django.shortcuts import render
from django.views.generic import View
from cerberus import Validator
from django.contrib.auth import authenticate, login
from django.db.models import Q
from django.contrib.auth.mixins import LoginRequiredMixin
import json
from .custom_validator import CustomValidator

class UserRegister(View):
       
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
            User.objects.create_user(username=data['username'],email=data['email'], 
                password=data['password'], first_name=data['first_name'],
                last_name=data['last_name'])
            return JsonResponse({
                "message" : "user successfully created"
                }, status=201)
        # in case username or email already exists in database we return that message
        else:
            return HttpResponseBadRequest({
                "errors":[{"message" : "user with that credentials already exists",
                "code": "registration.user_exists"}]
                }, status=460)


class UserLogin(View):
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


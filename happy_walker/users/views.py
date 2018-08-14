from django import forms
from django.contrib.auth.models import User
from django.http import HttpResponse, HttpRequest, JsonResponse
from django.http import HttpResponseRedirect, HttpResponseBadRequest
from django.shortcuts import render
from django.views.generic import View
from cerberus import Validator
from django.contrib.auth import authenticate
import re
from django.db.models import Q
import json
from . import custom_validator as cv

class ValidationView(View):
    schema = {}

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
            errors_dict = {
                'errors': []
            }

            for key, value in data_validator.errors.items():
                index = 0
                for err in range(len(data_validator.document_error_tree[key].errors)):
                    errors_dict['errors'].append({
                        "field": key,
                        "code": data_validator.document_error_tree[key].errors[index].rule,
                        "message": value[index]
                    })
                    index += 1

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
        if self.request_validation(request):
            errors_dict = self.request_validation(request)
            return JsonResponse(errors_dict, status = 400)
        else:
            data = json.loads(request.body)

        if not(User.objects.filter(
             Q(username=data['username']) |
             Q(email=data['email'])
             ).exists()):
            User.objects.create_user(username=data['username'],email=data['email'], 
                password=data['password'], first_name=data['firstname'],
                last_name=data['lastname'])
            return HttpResponse('HTTP_201_CREATED', status=201)
        # in case username or email already exists in database we return that message
        else:
            return HttpResponseBadRequest('HTTP_460_ALREADY_EXIST', status=460)


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
        if self.request_validation(request):
            errors_dict = self.request_validation(request)
            return JsonResponse(errors_dict, status = 400)
        else:
            data = json.loads(request.body)

        existing_user = User.objects.filter(Q(username=data['username_or_email']) |
            Q(email=data['username_or_email'])).get()
    
        if existing_user:
            user = authenticate(username=existing_user.username, 
                                             password=data['password'])
            if user is not None:
                return HttpResponse('success', status=230)
            else:
                return HttpResponseBadRequest("incorrect password", status=467)
        else:
            return HttpResponseBadRequest("user does not exist", status=432)
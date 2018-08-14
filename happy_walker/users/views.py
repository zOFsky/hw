from django import forms
from django.contrib.auth.models import User
from django.http import HttpResponse, HttpRequest, JsonResponse
from django.http import HttpResponseRedirect, HttpResponseBadRequest
from django.shortcuts import render
from django.views.generic import View
from cerberus import Validator
import re
from django.db.models import Q
import json
from . import custom_validator as cv

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
        if len(request.body) > 0 and len(request.FILES) == 0:
            data = json.loads(request.body)        
        
        # Validating password and email using cerberus library
        # validation schema is coded in validation.py file
         
        data_validator = Validator(self.validation_schema, 
                                   error_handler=cv.CustomErrorHandler)
        data_validator.allow_unknown = True
        data_validator(data)

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

            return JsonResponse(errors_dict, status = 400)

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



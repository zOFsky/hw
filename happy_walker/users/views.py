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


class UserRegister(View):
       
    validation_schema = {
        'password': {
            'type': 'string', 
            'minlength': 6, 
            'required': True
            },
        'email': {
            'required': True,
            'type': 'string', 
            'regex': '^[a-zA-Z0-9_.+-]+@[a-zA-Z0-9-]+\.[a-zA-Z0-9-.]+$',
            },
    }
    
    def post(self, request):
        if len(request.body) > 0 and len(request.FILES) == 0:
            data = json.loads(request.body)        
        
        # Validating password and email using cerberus library
        # validation schema is coded in validation.py file
         
        data_validator = Validator(self.validation_schema)
        data_validator.allow_unknown = True
        data_validator(data)

        #if there are errors we return them in HttpResponse
        if data_validator.errors:
            # errors_dict = {
            #     'errors':[]
            # }
            # for key, value in data_validator.errors.items():
            #    errors_dict['errors'].append({"message":key , "code": value[0]})
            
            # print("ERRORS: {}".format(data_validator.errors))
            errors_list = '' 
            for key, value in data_validator.errors.items():
                errors_list += str(key) + " : "  + str(value) + " \n "
            return HttpResponseBadRequest("HTTP_400_BAD_REQUEST \n " + errors_list)

            {
    "errors": [
        {"message": "everything failed!!11", "code": "registration.everything_failed"}
    ]
}


        
        # checking if username or email already exists
        # if not we create and add to database new user
        if not(User.objects.filter(
             Q(username=data['username']) |
             Q(email=data['email'])
             ).exists()):
            User.objects.create_user(username=data['username'],email=data['email'], 
                password=data['password'], first_name=data['firstname'],
                last_name=data['lastname'])
            return HttpResponse('HTTP_201_CREATED')
        # in case username or email already exists in database we return that message
        else:
            return HttpResponseBadRequest('HTTP_460_ALREADY_EXIST')



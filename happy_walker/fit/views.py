import time, datetime
from django.contrib.auth.models import User
from .models import FitDataModel
from users.models import Profile
from django.http import JsonResponse
from django.conf import settings
from django.shortcuts import redirect
#from django.http import HttpResponseRedirect, HttpResponseBadRequest
#from django.template.loader import get_template
from django.views.generic import View
#from django.contrib.auth import authenticate, login, logout
from django.db.models import Q, Avg, Sum
from django.core.exceptions import ObjectDoesNotExist
#from django.contrib.auth.mixins import LoginRequiredMixin
#from google_auth_oauthlib.flow import Flow
import google.oauth2.credentials
import googleapiclient.discovery
import json
#from .custom_validator import CustomValidator
#from .tokens import TokenGenerator
#from .email_sender import EmailSender
from . import epochtime
from .json_handlers import get_value_from_json, create_json_request
# Create your views here.

class FitDataView(View):
    def get(self, request):

        profile = Profile.objects.get(user_id=request.user.id)
        
        credentials = google.oauth2.credentials.Credentials(profile.access_token,
                                                            client_id=settings.CLIENT_ID,
                                                            client_secret=settings.CLIENT_SECRET,
                                                            refresh_token=profile.refresh_token,
                                                            token_uri=settings.TOKEN_URI)

        fit = googleapiclient.discovery.build(
            'fitness', 'v1', credentials=credentials)

        
        current_time = epochtime.date_to_epoch() * 1000
        week = epochtime.week * 1000
        day = epochtime.day

        
        data_list = [{"dataTypeName": "com.google.step_count.delta"},
                     {"dataTypeName": "com.google.distance.delta"},
                     {"dataTypeName": "com.google.calories.expended"}
                    ]
        bucket_dict = { "durationMillis": epochtime.day }

        data_request = create_json_request(aggregateBy=data_list,
            bucketByTime=bucket_dict, startTimeMillis=(current_time - epochtime.month),
            endTimeMillis=(current_time+day))
        
        # distance_request = create_json_request(aggregateBy=distance_list,
        #     bucketByTime=bucket_dict, startTimeMillis=(current_time - epochtime.week),
        #     endTimeMillis=current_time)

        # calor_request = create_json_request(aggregateBy=calor_list,
        #     bucketByTime=bucket_dict, startTimeMillis=(current_time - epochtime.week),
        #     endTimeMillis=current_time)

        fit_data = fit.users().dataset().aggregate(userId='me', 
            body=json.loads(data_request)).execute()
        
        Profile.objects.filter(user_id=profile.user_id).update(access_token=credentials.token,
                                                               refresh_token=credentials.refresh_token)

        # distance_data = fit.users().dataset().aggregate(userId='me', 
        #     body=json.loads(distance_request)).execute()

        # calor_data = fit.users().dataset().aggregate(userId='me', 
        #     body=json.loads(calor_request)).execute()
        
        list_by_days = get_value_from_json(json.dumps(fit_data))
        dict_by_days = { i : list_by_days[i] for i in range(0, len(list_by_days)) }
        #return JsonResponse(fit_data)
        return JsonResponse(dict_by_days)


class SaveFitDataView(View):
    def get(self, request):
        if 'credentials' not in request.session:
            return redirect('/oauth')

        credentials = request.session['credentials']

        credentials = google.oauth2.credentials.Credentials(
            token=credentials['token'],
            refresh_token=credentials['refresh_token'],
            token_uri=credentials['token_uri'],
            client_id=credentials['client_id'],
            client_secret=credentials['client_secret'],
            scopes=credentials['scopes'])

        fit = googleapiclient.discovery.build(
            'fitness', 'v1', credentials=credentials)

        
        current_time = epochtime.date_to_epoch() * 1000
        week = epochtime.week * 1000
        day = epochtime.day

        data_list = [{"dataTypeName": "com.google.step_count.delta"},
                     {"dataTypeName": "com.google.distance.delta"},
                     {"dataTypeName": "com.google.calories.expended"}
                    ]
        bucket_dict = { "durationMillis": epochtime.day }

        data_request = create_json_request(aggregateBy=data_list,
            bucketByTime=bucket_dict, startTimeMillis=(current_time - epochtime.month),
            endTimeMillis=(current_time+day))

        fit_data = fit.users().dataset().aggregate(userId='me', 
            body=json.loads(data_request)).execute()
        
        list_by_days = get_value_from_json(json.dumps(fit_data))
        dict_by_days = { i : list_by_days[i] for i in range(0, len(list_by_days)) 
                       }
        user = User.objects.get(username='myusername')
        for elem in list_by_days:
            if not(FitDataModel.objects.filter(user=user, 
                                               date=elem["date"]).exists()):
                day_data = FitDataModel(user=user, date=elem['date'],
                        steps=elem["steps"], distance=elem["distance"],
                        calories=elem["calories"])
                day_data.save()
            else:
                FitDataModel.objects.filter(user=user,date=elem["date"]).update(
                                                steps=elem["steps"], 
                                                distance=elem["distance"],
                                                calories=elem["calories"]
                                                )
        return JsonResponse({
                'message':'We saved data in myusername'
            }, status=200)
    

class LastNDaysView(View):
    def get(self, request):
        user = User.objects.get(username="myusername")
        since_data = datetime.date.today() - datetime.timedelta(days=3)
        # total_steps = FitDataModel.objects.filter(user=user, 
        #                             date__gt=since_data).aggregate(Avg('steps'))
        total_steps = FitDataModel.objects.filter(user=user,
                                                  date__gt=since_data).aggregate(Sum('steps'))
        return JsonResponse({
                'message':'Here are results for your last days', 
                'steps for 3 days': total_steps
            }, status=200)
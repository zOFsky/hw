import datetime
from django.contrib.auth.models import User
from .models import FitDataModel
from users.models import Profile
from django.http import JsonResponse
from django.conf import settings
from django.views.generic import View
from django.db.models import Sum
import google.oauth2.credentials
import googleapiclient.discovery
import json
from . import epochtime
from .json_handlers import get_value_from_json, create_json_request, get_value_from_json_by_hours
# Create your views here.

class SaveFitDataView(View):
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
        day = epochtime.day

        data_list = [
            {"dataTypeName": "com.google.step_count.delta"},
            {"dataTypeName": "com.google.distance.delta"},
            {"dataTypeName": "com.google.calories.expended"}
            ]

        bucket_dict = {"durationMillis": epochtime.day}
        
        data_request = create_json_request(aggregateBy=data_list,
            bucketByTime=bucket_dict, startTimeMillis=(current_time-epochtime.day*73),
            endTimeMillis=(current_time+day))
        fit_data = fit.users().dataset().aggregate(userId='me', 
            body=json.loads(data_request)).execute()
        
        Profile.objects.filter(user_id=profile.user_id).update(access_token=credentials.token)

        list_by_days = get_value_from_json(json.dumps(fit_data))
        #dict_by_days = { i : list_by_days[i] for i in range(0, len(list_by_days)) }
        
        user = User.objects.get(username=request.user.username)
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
#-----------------------------------------------
        for i in range(1, 2):
            data_request = create_json_request(aggregateBy=data_list,
                bucketByTime=bucket_dict, startTimeMillis=(current_time - (i+1)*epochtime.day*73),
                endTimeMillis=(current_time-i*epochtime.day*73+day))
      
            fit_data = fit.users().dataset().aggregate(userId='me', 
                body=json.loads(data_request)).execute()
            
            list_by_days = get_value_from_json(json.dumps(fit_data))
         #   dict_by_days = { i : list_by_days[i] for i in range(0, len(list_by_days)) }
            
            user = User.objects.get(username=request.user.username)
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
                'message': f'We saved data in {user.username}'
            }, status=200)
        #return JsonResponse(fit_data)
        #return JsonResponse(dict_by_days)

class TopWalkersView(View):
    def get(self, request, req_days):
        user = User.objects.get(id=request.user.id)
        if user.profile.location.city == '':
            return JsonResponse({'top_walkers': []}, status=200)

        lat = user.profile.location.lat
        lng = user.profile.location.lng

        since_data = datetime.date.today() - datetime.timedelta(days=req_days)
        n = 0
        final_list = []
        for fit_record in User.objects \
                    .filter(user_fit__date__gt=since_data, profile__location=user.profile.location) \
                    .annotate(total_steps=Sum('user_fit__steps'), 
                            total_distance=Sum('user_fit__distance'),
                            total_calories=Sum('user_fit__calories')) \
                    .values('first_name', 'last_name', 'total_steps',
                            'total_distance', 'total_calories', 'id') \
                    .order_by('-total_steps'):
            n=n+1

            final_list.append(
                {
                    "id": fit_record['id'],
                    "position": n,
                    "first_name": fit_record['first_name'],
                    "last_name": fit_record['last_name'],
                    "steps": fit_record['total_steps'],
                    "distance": fit_record['total_distance'],
                    "calories": fit_record['total_calories'],
                    "image": Profile.objects.get(user_id=fit_record['id']).get_image()
                }
            )  

        users_data = {
            'top walkers': final_list
        }
 
        #return JsonResponse({'result':str(result)})
        return JsonResponse(users_data, status=200)

class UserFitDataView(View):
    def get(self, request, req_days):
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
        if req_days == 1:
            bucket_hour = { "durationMillis": epochtime.hour }
            data_request = create_json_request(aggregateBy=data_list,
                bucketByTime=bucket_hour, startTimeMillis=(current_time),
                endTimeMillis=(current_time+day))
            fit_data = fit.users().dataset().aggregate(userId='me', 
                body=json.loads(data_request)).execute()
            Profile.objects.filter(user_id=profile.user_id).update(access_token=credentials.token)
            list_by_hours = get_value_from_json_by_hours(json.dumps(fit_data))
            dict_by_hours = { i : list_by_hours[i] for i in range(0, len(list_by_hours)) }
            return JsonResponse(dict_by_hours, status=200)
        elif req_days < 75:
            # data_list = [{"dataTypeName": "com.google.step_count.delta"},
            #             {"dataTypeName": "com.google.distance.delta"},
            #             {"dataTypeName": "com.google.calories.expended"}
            #             ]
            # bucket_dict = { "durationMillis": epochtime.day }

            data_request = create_json_request(aggregateBy=data_list,
                bucketByTime=bucket_dict, startTimeMillis=(current_time - epochtime.day*(req_days-1)),
                endTimeMillis=(current_time+day))
            
            fit_data = fit.users().dataset().aggregate(userId='me', 
                body=json.loads(data_request)).execute()
            
            Profile.objects.filter(user_id=profile.user_id).update(access_token=credentials.token)

            list_by_days = get_value_from_json(json.dumps(fit_data))
            dict_by_days = { i : list_by_days[i] for i in range(0, len(list_by_days)) }
            
            return JsonResponse(dict_by_days, status=200)
        else:
            # data_list = [{"dataTypeName": "com.google.step_count.delta"},
            #             {"dataTypeName": "com.google.distance.delta"},
            #             {"dataTypeName": "com.google.calories.expended"}
            #             ]
            # bucket_dict = { "durationMillis": epochtime.day }
            data_request = create_json_request(aggregateBy=data_list,
                bucketByTime=bucket_dict, startTimeMillis=(current_time - epochtime.day*(req_days-1)),
                endTimeMillis=(current_time+day))
            
            fit_data = fit.users().dataset().aggregate(userId='me', 
                body=json.loads(data_request)).execute()
            
            Profile.objects.filter(user_id=profile.user_id).update(access_token=credentials.token)

            list_by_days = list_by_days = get_value_from_json(json.dumps(fit_data))
            for i in range(1,5):
                data_request = create_json_request(aggregateBy=data_list,
                         bucketByTime=bucket_dict, startTimeMillis=(current_time - (i+1)*epochtime.day*73),
                         endTimeMillis=(current_time-i*epochtime.day*73))
                fit_data = fit.users().dataset().aggregate(userId='me', 
                    body=json.loads(data_request)).execute()
                
                list_by_days = get_value_from_json(json.dumps(fit_data)) + list_by_days

            dict_by_days = { i : list_by_days[i] for i in range(0, len(list_by_days)) }
            
            return JsonResponse(dict_by_days, status=200)
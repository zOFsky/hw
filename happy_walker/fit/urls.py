from django.urls import path
from .views import *
from django.views.decorators.csrf import csrf_exempt

urlpatterns = [
    path('fit_data', csrf_exempt(FitDataView.as_view()), name='fit_data'),    
    path('last_days', csrf_exempt(LastNDaysView.as_view()), name='last_days'),
    path('save_fit_data', csrf_exempt(SaveFitDataView.as_view()), name='save_fit_data'),
]
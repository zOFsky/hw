from django.urls import path
from .views import *
from django.views.decorators.csrf import csrf_exempt

urlpatterns = [
    #path('fit_data', csrf_exempt(FitDataView.as_view()), name='fit_data'),    
    path('top_walkers/<int:req_days>', csrf_exempt(TopWalkersView.as_view()), name='top_walkers'),
    path('save_fit_data', csrf_exempt(SaveFitDataView.as_view()), name='save_fit_data'),
    path('user_data', csrf_exempt(UserFitDataView.as_view()), name='user_data'),
]
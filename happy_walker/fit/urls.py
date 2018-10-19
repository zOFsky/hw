from django.urls import path
from .views import *
from django.contrib.auth.decorators import login_required


urlpatterns = [
    path('top_walkers/<int:req_days>', login_required(TopWalkersView.as_view()), name='top_walkers'),
    path('save_fit_data', login_required(SaveFitDataView.as_view()), name='save_fit_data'),
    path('user_data/<int:req_days>', login_required(UserFitDataView.as_view()), name='user_data'),
]
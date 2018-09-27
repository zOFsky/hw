from django.urls import path, include
from users.views import Oauth2Callback

urlpatterns = [
    path('', include('home.urls')),
    path('users/', include('users.urls')),
    path('oauth2callback', Oauth2Callback.as_view(), name='oauth2callback'),
]

from django.urls import path, include
from django.contrib import admin
from users.views import Oauth2Callback

urlpatterns = [
    path('', include('home.urls')),
    path('users/', include('users.urls')),
    path('admin/', admin.site.urls),
    path('oauth2callback', Oauth2Callback.as_view(), name='oauth2callback'),
]

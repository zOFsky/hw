from django.urls import path, include
from django.views.decorators.csrf import csrf_exempt

urlpatterns = [
    path('', include('home.urls')),
    path('users/', include('users.urls')),
    path('users/', csrf_exempt(include('django.contrib.auth.urls'))),

]

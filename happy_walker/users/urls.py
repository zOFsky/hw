from django.urls import path
from .views import UserRegister
from django.views.decorators.csrf import csrf_exempt


urlpatterns = [
    path('register', csrf_exempt(UserRegister.as_view()), name='register'),
]
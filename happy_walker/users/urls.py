from django.urls import path
from .views import UserRegister, UserLogin, UserUpdateProfile
from django.views.decorators.csrf import csrf_exempt


urlpatterns = [
    path('register', csrf_exempt(UserRegister.as_view()), name='register'),
    path('sign-in', UserLogin.as_view(), name='login'),
    path('me', UserUpdateProfile.as_view(), name='update'),
]
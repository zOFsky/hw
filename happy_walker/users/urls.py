from django.urls import path
from .views import UserRegister, UserLogin, ConfirmEmail, Profile
from django.views.decorators.csrf import csrf_exempt
from django.contrib.auth.decorators import login_required


urlpatterns = [
    path('register', csrf_exempt(UserRegister.as_view()), name='register'),
    path('confirm_email', csrf_exempt(ConfirmEmail.as_view()), name='confirm_email'),
    path('<user_id>', login_required(csrf_exempt(Profile.as_view())), name='profile'),
    path('sign-in', UserLogin.as_view(), name='login'),
]
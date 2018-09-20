from django.urls import path
from .views import (UserRegisterView, UserLoginView, ConfirmEmailView, 
                   ChangeEmailView, ProfileView, ChangePasswordView)
from django.views.decorators.csrf import csrf_exempt
from django.contrib.auth.decorators import login_required


urlpatterns = [
    path('register', csrf_exempt(UserRegisterView.as_view()), name='register'),
    path('confirm_email', csrf_exempt(ConfirmEmailView.as_view()), name='confirm_email'),
    path('change_email', csrf_exempt(ChangeEmailView.as_view()), name='change_email'),
    path('sign_in', csrf_exempt(UserLoginView.as_view()), name='login'),
    path('change_password', ChangePasswordView.as_view(), name='change_password'),
    path('<user_id>', login_required(csrf_exempt(ProfileView.as_view())), name='profile'),
    
]
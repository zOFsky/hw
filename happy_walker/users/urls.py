from django.urls import path
from .views import (UserRegisterView, UserLoginView, ConfirmEmailView, ForgotPasswordView,
                   ChangeEmailView, ProfileView, ChangePasswordView, ResetPasswordView, UploadPhotoView)
from django.views.decorators.csrf import csrf_exempt
from django.contrib.auth.decorators import login_required


urlpatterns = [
    path('register', csrf_exempt(UserRegisterView.as_view()), name='register'),
    path('confirm_email', csrf_exempt(ConfirmEmailView.as_view()), name='confirm_email'),
    path('change_email', csrf_exempt(login_required(ChangeEmailView.as_view())), name='change_email'),
    path('sign_in', csrf_exempt(UserLoginView.as_view()), name='login'),
    path('change_password', login_required(csrf_exempt(ChangePasswordView.as_view())), name='change_password'),
    path('forgot_password', csrf_exempt(ForgotPasswordView.as_view()), name='forgot_password'),
    path('reset_password', csrf_exempt(ResetPasswordView.as_view()), name='reset_password'),
    path('upload_photo', csrf_exempt(login_required(UploadPhotoView.as_view())), name='image'),
    path('<user_id>', login_required(csrf_exempt(ProfileView.as_view())), name='profile'),
]


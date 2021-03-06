from django.urls import path
from .views import *
from django.views.decorators.csrf import csrf_exempt
from django.contrib.auth.decorators import login_required


urlpatterns = [
    path('register', csrf_exempt(UserRegisterView.as_view()), name='register'),
    path('confirm_email', csrf_exempt(ConfirmEmailView.as_view()), name='confirm_email'),
    path('resend_email/<user_id>', csrf_exempt(ResendEmailView.as_view()), name='resend_email'),
    path('change_email', login_required(ChangeEmailView.as_view()), name='change_email'),
    path('sign_in', csrf_exempt(UserLoginView.as_view()), name='login'),
    path('change_password', login_required(csrf_exempt(ChangePasswordView.as_view())), name='change_password'),
    path('logout', UserLogoutView.as_view(), name='logout'),
    path('forgot_password', csrf_exempt(ForgotPasswordView.as_view()), name='forgot_password'),
    path('reset_password', csrf_exempt(ResetPasswordView.as_view()), name='reset_password'),
    path('upload_photo', login_required(UploadPhotoView.as_view()), name='image'),
    path('oauth', csrf_exempt(OAuthView.as_view()), name='oauth'),
    path('credentials', csrf_exempt(CredentialsView.as_view()), name='credentials'),
    path('top_walkers', login_required(TopWalkersView.as_view()), name='top_walkers'),
    path('favorite/<favorite_id>', login_required(FavoritesView.as_view()), name='favorites'),
    path('<user_id>', login_required(ProfileView.as_view()), name='profile'),
]

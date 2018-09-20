from django.urls import path
from .views import (UserRegisterView, UserLoginView, ConfirmEmailView, 
                   ChangeEmailView, ProfileView, Image)
from django.views.decorators.csrf import csrf_exempt
from django.contrib.auth.decorators import login_required
from django.conf.urls.static import static
from django.conf import settings


urlpatterns = [
    path('register', csrf_exempt(UserRegisterView.as_view()), name='register'),
    path('confirm_email', csrf_exempt(ConfirmEmailView.as_view()), name='confirm_email'),
    path('change_email', login_required(ChangeEmailView.as_view()), name='change_email'),
    path('sign_in', csrf_exempt(UserLoginView.as_view()), name='login'),
    path('image', csrf_exempt(login_required(Image.as_view())), name='image'),
    path('<user_id>', csrf_exempt(login_required(ProfileView.as_view())), name='profile')
] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
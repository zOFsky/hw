from django.urls import path, include

urlpatterns = [
    path('', include('home.urls')),
    path('users/', include('users.urls')),
]

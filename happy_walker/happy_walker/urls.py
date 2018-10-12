from django.urls import path, include
from django.contrib import admin

urlpatterns = [
    path('', include('home.urls')),
    path('users/', include('users.urls')),
    path('admin/', admin.site.urls),
]

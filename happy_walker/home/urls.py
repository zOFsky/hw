from django.urls import path
from . import views
from django.views.generic.base import RedirectView

urlpatterns = [
    path('', views.homepage, name='home'),
    path('api', RedirectView.as_view(url='/static/api/swagger-ui/dist/index.html?url=/static/HappyWalker.yaml'),
         name='api'),
]

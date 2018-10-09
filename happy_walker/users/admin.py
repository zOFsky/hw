from django.contrib import admin
from django.contrib.auth.models import User
from .models import Profile, FitDataModel

# Register your models here.
#admin.site.register(User)
admin.site.register(Profile)
admin.site.register(FitDataModel)
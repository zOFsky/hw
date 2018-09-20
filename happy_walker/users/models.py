from django.db import models
from django.contrib.auth import get_user_model
from django.db.models.signals import post_save
from django.dispatch import receiver


class Profile(models.Model):
    user = models.OneToOneField(get_user_model(), on_delete=models.CASCADE)
    gender = models.CharField(max_length=20, blank=True)
    age = models.IntegerField(blank=True)
    weight = models.IntegerField(blank=True)
    image = models.ImageField(upload_to='images/photos')

@receiver(post_save, sender=get_user_model())
def create_user_profile(sender, instance, created, **kwargs):
    if created:
        Profile.objects.create(user=instance)

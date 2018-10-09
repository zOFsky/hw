from django.db import models
from django.contrib.auth import get_user_model
from django.db.models.signals import post_save
from django.dispatch import receiver


class Profile(models.Model):
    user = models.OneToOneField(get_user_model(), on_delete=models.CASCADE)
    image = models.ImageField(upload_to='images/photos', default='images/avatar.png')

    def __str__(self):
        return self.user

@receiver(post_save, sender=get_user_model())
def create_user_profile(sender, instance, created, **kwargs):
    if created:
        Profile.objects.create(user=instance)

class FitDataModel(models.Model):
    user = models.ForeignKey(get_user_model(), on_delete=models.CASCADE)
    date = models.DateField(unique=True)
    steps = models.IntegerField(default=0)
    distance = models.FloatField(default=0)
    calories = models.FloatField(default=0)

    def __str__(self):
        return f'{self.user} {self.date} {self.steps}'

    class Meta:
        ordering = ['-date']
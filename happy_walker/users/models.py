from djongo import models
from django.contrib.auth import get_user_model
from django.db.models.signals import post_save
from django.dispatch import receiver


class Location(models.Model):
    lat = models.FloatField()
    lng = models.FloatField()
    city = models.TextField()

    class Meta:
        abstract = True


class Profile(models.Model):
    user = models.OneToOneField(get_user_model(), on_delete=models.CASCADE)
    image = models.ImageField(upload_to='images/photos', default='images/avatar.png')
    favorites = models.ListField(default=[])
    location = models.EmbeddedModelField(
        model_container=Location,
    )

    objects = models.DjongoManager()


@receiver(post_save, sender=get_user_model())
def create_user_profile(sender, instance, created, **kwargs):
    if created:
        Profile.objects.create(user=instance, location=Location())

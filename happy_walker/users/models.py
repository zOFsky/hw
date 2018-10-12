from djongo import models
from django.contrib.auth import get_user_model
from django.db.models.signals import post_save
from django.dispatch import receiver
import cloudinary.models as cloudinary


class Location(models.Model):
    lat = models.FloatField()
    lng = models.FloatField()
    city = models.TextField()

    class Meta:
        abstract = True


class Profile(models.Model):
    user = models.OneToOneField(get_user_model(), on_delete=models.CASCADE)
    image = cloudinary.CloudinaryField('image')
    google_image = models.CharField(max_length=255, null=True)
    favorites = models.ListField(default=[])
    location = models.EmbeddedModelField(
        model_container=Location,
    )
    access_token = models.CharField(max_length=255, null=True)
    refresh_token = models.CharField(max_length=255, null=True)

    objects = models.DjongoManager()


@receiver(post_save, sender=get_user_model())
def create_user_profile(sender, instance, created, **kwargs):
    if created:
        Profile.objects.create(user=instance, location=Location())

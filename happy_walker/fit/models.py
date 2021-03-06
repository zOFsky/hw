from django.db import models
from django.contrib.auth import get_user_model


class FitDataModel(models.Model):
    user = models.ForeignKey(get_user_model(), on_delete=models.CASCADE, related_name = "user_fit")
    date = models.DateField()
    steps = models.IntegerField(default=0)
    distance = models.FloatField(default=0)
    calories = models.FloatField(default=0)

    def __str__(self):
        return f'{self.user.username} {self.date} {self.steps}'

    class Meta:
        ordering = ['-user']


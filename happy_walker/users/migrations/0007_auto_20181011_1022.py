# Generated by Django 2.0.7 on 2018-10-11 10:22

import cloudinary.models
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('users', '0006_remove_profile_google_image'),
    ]

    operations = [
        migrations.AddField(
            model_name='profile',
            name='google_image',
            field=models.CharField(max_length=255, null=True),
        ),
        migrations.AlterField(
            model_name='profile',
            name='image',
            field=cloudinary.models.CloudinaryField(max_length=255, verbose_name='image'),
        ),
    ]
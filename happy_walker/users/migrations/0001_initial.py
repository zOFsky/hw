# Generated by Django 2.0.7 on 2018-10-11 10:28

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion
import djongo.models.fields
import users.models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.CreateModel(
            name='Profile',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('image', models.ImageField(null=True, upload_to='images/photos')),
                ('google_image', models.CharField(max_length=255, null=True)),
                ('favorites', djongo.models.fields.ListField(default=[])),
                ('location', djongo.models.fields.EmbeddedModelField(model_container=users.models.Location, null=True)),
                ('access_token', models.CharField(max_length=255, null=True)),
                ('refresh_token', models.CharField(max_length=255, null=True)),
                ('user', models.OneToOneField(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL)),
            ],
        ),
    ]

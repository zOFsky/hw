# Generated by Django 2.0.7 on 2018-10-03 07:56

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion
import djongo.models.fields
import users.models


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('users', '0001_initial'),
    ]

    operations = [
        migrations.CreateModel(
            name='OAuthData',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('token', models.CharField(max_length=255)),
                ('refresh_token', models.CharField(max_length=255)),
                ('token_uri', models.CharField(max_length=255)),
                ('client_id', models.CharField(max_length=255)),
                ('client_secret', models.CharField(max_length=255)),
                ('scopes', djongo.models.fields.ListField()),
                ('user', models.OneToOneField(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL)),
            ],
        ),
        migrations.AddField(
            model_name='profile',
            name='favorites',
            field=djongo.models.fields.ListField(default=[]),
        ),
        migrations.AddField(
            model_name='profile',
            name='location',
            field=djongo.models.fields.EmbeddedModelField(model_container=users.models.Location, null=True),
        ),
    ]

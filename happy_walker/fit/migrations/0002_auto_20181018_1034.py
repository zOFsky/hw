# Generated by Django 2.0.7 on 2018-10-18 10:34

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('fit', '0001_initial'),
    ]

    operations = [
        migrations.AlterField(
            model_name='fitdatamodel',
            name='user',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='user_fit', to=settings.AUTH_USER_MODEL),
        ),
    ]
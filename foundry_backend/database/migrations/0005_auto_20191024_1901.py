# Generated by Django 2.2.5 on 2019-10-24 19:01

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('database', '0004_auto_20191024_1901'),
    ]

    operations = [
        migrations.AlterField(
            model_name='mlsnumber',
            name='user',
            field=models.OneToOneField(null=True, on_delete=django.db.models.deletion.CASCADE, related_name='mls_number', to=settings.AUTH_USER_MODEL),
        ),
    ]
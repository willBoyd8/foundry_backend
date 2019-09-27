# Generated by Django 2.2.5 on 2019-09-26 18:47

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('database', '0005_auto_20190926_1807'),
    ]

    operations = [
        migrations.AddField(
            model_name='mlsnumber',
            name='owner',
            field=models.ForeignKey(null=True, on_delete=django.db.models.deletion.CASCADE, related_name='mls_number', to=settings.AUTH_USER_MODEL),
        ),
    ]

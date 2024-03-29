# Generated by Django 2.2.5 on 2019-11-23 17:23

from django.db import migrations, models
import django.utils.timezone


class Migration(migrations.Migration):

    dependencies = [
        ('database', '0024_showingreview'),
    ]

    operations = [
        migrations.AddField(
            model_name='listing',
            name='date_posted',
            field=models.DateTimeField(auto_now_add=True, default=django.utils.timezone.now),
            preserve_default=False,
        ),
        migrations.AddField(
            model_name='listing',
            name='open',
            field=models.BooleanField(default=True),
        ),
    ]

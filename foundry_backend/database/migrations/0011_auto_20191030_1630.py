# Generated by Django 2.2.5 on 2019-10-30 16:30

import datetime
from django.db import migrations, models
from django.utils.timezone import utc


class Migration(migrations.Migration):

    dependencies = [
        ('database', '0010_auto_20191030_1510'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='showing',
            name='duration',
        ),
        migrations.AddField(
            model_name='showing',
            name='end_time',
            field=models.DateTimeField(default=datetime.datetime(2019, 10, 30, 16, 30, 57, 783828, tzinfo=utc)),
            preserve_default=False,
        ),
    ]
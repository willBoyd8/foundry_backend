# Generated by Django 2.2.5 on 2019-11-06 02:53

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('database', '0011_auto_20191030_1630'),
    ]

    operations = [
        migrations.AlterField(
            model_name='homealarm',
            name='property',
            field=models.OneToOneField(on_delete=django.db.models.deletion.CASCADE, related_name='home_alarm', to='database.Property'),
        ),
    ]

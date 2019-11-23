# Generated by Django 2.2.5 on 2019-11-23 18:28

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('database', '0025_auto_20191123_1123'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='nearbyattraction',
            name='properties',
        ),
        migrations.AddField(
            model_name='nearbyattraction',
            name='property',
            field=models.ForeignKey(default=1, on_delete=django.db.models.deletion.CASCADE, related_name='nearby_attractions', to='database.Property'),
            preserve_default=False,
        ),
    ]
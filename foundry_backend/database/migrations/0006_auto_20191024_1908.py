# Generated by Django 2.2.5 on 2019-10-24 19:08

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('database', '0005_auto_20191024_1901'),
    ]

    operations = [
        migrations.AlterField(
            model_name='mlsnumber',
            name='agency',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='mls_numbers', to='database.Agency'),
        ),
    ]

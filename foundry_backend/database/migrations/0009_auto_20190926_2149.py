# Generated by Django 2.2.5 on 2019-09-26 21:49

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('database', '0008_auto_20190926_2054'),
    ]

    operations = [
        migrations.RenameField(
            model_name='mlsnumber',
            old_name='owner',
            new_name='user',
        ),
    ]

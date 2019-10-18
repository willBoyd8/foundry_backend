# Generated by Django 2.2.5 on 2019-10-18 16:31

from django.db import migrations, models
import django.db.models.deletion
import multiselectfield.db.fields


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='IAMPolicy',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=255, unique=True)),
                ('notes', models.CharField(blank=True, max_length=255, null=True)),
            ],
        ),
        migrations.CreateModel(
            name='IAMPolicyRule',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('notes', models.CharField(blank=True, max_length=255, null=True)),
                ('actions', multiselectfield.db.fields.MultiSelectField(choices=[('list', 'List all objects (GET)'), ('retrieve', 'Retrieve a specific object (GET with PK)'), ('create', 'Create a new object (POST)'), ('update', "Update a specific object in it's entirety (PUT)"), ('update_partial', "Update a specific object's specific elements (PATCH)"), ('delete', 'Delete an object (DELETE)'), ('all', 'All actions'), ('safe', 'Read only actions')], max_length=58)),
                ('effect', models.CharField(choices=[('allow', 'This rule allows users permission'), ('deny', 'This rule denies users permission')], max_length=5)),
                ('list', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='rules', to='api.IAMPolicy')),
            ],
        ),
        migrations.CreateModel(
            name='IAMPrincipalItem',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('value', models.CharField(max_length=255)),
                ('policy', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='principals', to='api.IAMPolicyRule')),
            ],
        ),
        migrations.CreateModel(
            name='IAMConditionItem',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('value', models.CharField(max_length=255)),
                ('policy', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='conditions', to='api.IAMPolicyRule')),
            ],
        ),
    ]

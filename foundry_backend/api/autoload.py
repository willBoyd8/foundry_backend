# autoload.py
#
# Foundry Backend
#
# This module defines the commands that should run on startup of
# the foundry_backend.
import json
import os

from django.conf import settings
from django.contrib.auth.models import User
from django.db import connection

from foundry_backend.api.models import IAMPolicy
from foundry_backend.api.serializers import IAMPolicySerializer


def load_json_access_policies(path: str):
    print('Deleting default authentication model...')
    IAMPolicy.objects.filter(name='default').delete()

    print('Creating authentication models')
    with open(path, 'r') as permissions_file:
        permissions_data = json.loads(str(permissions_file.read()))
        for perm in permissions_data:
            serializer = IAMPolicySerializer(data=perm)

            if serializer.is_valid():
                print('Saving Policy: \'{}\''.format(perm['name']))
                serializer.save()
            else:
                print('⚠️⚠️⚠️ Error adding \'{}\'⚠️⚠️⚠️'.format(perm['name']))
                print(serializer.errors)


def load_default_access_policies():
    load_json_access_policies(os.path.join(settings.BASE_DIR, settings.PERMISSIONS_JSON))


def load_wild_west_access_policies():
    IAMPolicy.objects.all().delete()

    load_json_access_policies(os.path.join(settings.BASE_DIR, settings.PERMISSIONS_JSON))


def create_default_admin():
    if not User.objects.filter(username='admin').exists():
        print('Could not find \'admin\' user. Creating now...')
        admin = User.objects.create_user(username=settings.ADMIN_USERNAME,
                                         password=settings.ADMIN_PASSWORD,
                                         email=settings.ADMIN_EMAIL)

        admin.is_staff = True
        admin.is_superuser = True

    else:
        print('Found \'admin\' user.')


def run():
    all_tables = connection.introspection.table_names()

    if len(all_tables) > 0:
        if settings.ENV_NAME == 'wild_west':
            print('⚠️🌵️🐎 WILD WEST MODE 🐎🌵️⚠️️ -  WILD WEST MODE WILL PURGE ALL PERMISSIONS FROM YOUR DATABASE.')
            print('⚠️🌵️🐎 WILD WEST MODE 🐎🌵️⚠️️ -  YOU WILL NEED TO REBUILD THE DATABASE PERMISSIONS AFTER THIS')
            print('⚠️🌵️🐎 WILD WEST MODE 🐎🌵️⚠️️ -  RUN. DO NOT RUN IN PRODUCTION')
            print('⚠️🌵️🐎 WILD WEST MODE 🐎🌵️⚠️️ -  Loading wild west authorization models')
            load_wild_west_access_policies()
        else:
            print('Loading default authorization models...')
            load_default_access_policies()

        create_default_admin()

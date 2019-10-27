# autoload.py
#
# Foundry Backend
#
# This module defines the commands that should run on startup of
# the foundry_backend.
import json
import os

from django.conf import settings
from django.db import connection

from foundry_backend.api.models import IAMPolicy
from foundry_backend.api.serializers import IAMPolicySerializer


def load_json_access_policies(path: str):
    all_tables = connection.introspection.table_names()

    if len(all_tables) > 0:
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
    else:
        print('WARNING: No tables were found in the database, so applying '
              '         IAM permissions was deferred to a later date. If '
              '         you are running in production, you have failed to'
              '         create IAM models and the application WILL FAIL')


def load_default_access_policies():
    load_json_access_policies(os.path.join(settings.BASE_DIR, settings.PERMISSIONS_JSON))


def load_wild_west_access_policies():
    IAMPolicy.objects.all().delete()

    load_json_access_policies(os.path.join(settings.BASE_DIR, settings.PERMISSIONS_JSON))


def run():
    if settings.ENV_NAME == 'wild_west':
        print('⚠️🌵️🐎 WILD WEST MODE 🐎🌵️⚠️️ -  WILD WEST MODE WILL PURGE ALL PERMISSIONS FROM YOUR DATABASE.')
        print('⚠️🌵️🐎 WILD WEST MODE 🐎🌵️⚠️️ -  YOU WILL NEED TO REBUILD THE DATABASE PERMISSIONS AFTER THIS')
        print('⚠️🌵️🐎 WILD WEST MODE 🐎🌵️⚠️️ -  RUN. DO NOT RUN IN PRODUCTION')
        print('⚠️🌵️🐎 WILD WEST MODE 🐎🌵️⚠️️ -  Loading wild west authorization models')
        load_wild_west_access_policies()
    else:
        print('Loading default authorization models...')
        load_default_access_policies()

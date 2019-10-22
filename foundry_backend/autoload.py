# autoload.py
#
# Foundry Backend
#
# This module defines the commands that should run on startup of
# the foundry_backend.
import json
import os
from foundry_backend.api.serializers import IAMPolicySerializer
from foundry_backend.api.models import IAMPolicy
from django.conf import settings


def load_json_access_policies(path: str):
    print('Deleting default authentication model...')
    IAMPolicy.objects.filter(name='default').delete()

    print('Creating authentication models')
    with open(path, 'r') as permissions_file:
        permissions_data = json.loads(str(permissions_file.read()))
        for perm in permissions_data:
            serializer = IAMPolicySerializer(data=perm)

            if serializer.is_valid():
                serializer.save()


def load_default_access_policies():
    load_json_access_policies(os.path.join(settings.BASE_DIR, 'deploy/default_permissions.json'))


def load_wild_west_access_policies():
    load_json_access_policies(os.path.join(settings.BASE_DIR, 'deploy/wild_west_permissions.json'))


def run():
    if settings.ENV_NAME == 'wild_west':
        print('⚠️🌵️🐎 WILD WEST MODE 🐎🌵️⚠️️ - DO NOT RUN IN PRODUCTION')
        print('⚠️🌵️🐎 WILD WEST MODE 🐎🌵️⚠️️ -  Loading wild west authorization models')
        load_wild_west_access_policies()
    else:
        print('Loading default authorization models...')
        load_default_access_policies()

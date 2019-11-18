import json
import logging
import os

from django.conf import settings
from foundry_backend.api.models import IAMPolicy
from foundry_backend.api.serializers import IAMPolicySerializer
from django.contrib.auth.models import User, Group


class AccessPolicyMiddleware:

    def _load_json_access_policies(self, path: str):
        self.logger.debug('Deleting default authentication model...')

        IAMPolicy.objects.filter(name='default').delete()

        self.logger.debug('Creating authentication models')
        with open(path, 'r') as permissions_file:
            permissions_data = json.loads(str(permissions_file.read()))
            for perm in permissions_data:
                serializer = IAMPolicySerializer(data=perm)

                if serializer.is_valid():
                    self.logger.debug('Saving Policy: \'{}\''.format(perm['name']))
                    serializer.save()
                else:
                    self.logger.warning('⚠️⚠️⚠️ Error adding \'{}\'⚠️⚠️⚠️'.format(perm['name']))
                    self.logger.warning(serializer.errors)

    def _load_default_access_policies(self):
        self._load_json_access_policies(os.path.join(settings.BASE_DIR, settings.PERMISSIONS_JSON))

    def _load_wild_west_access_policies(self):

        IAMPolicy.objects.all().delete()

        self._load_json_access_policies(os.path.join(settings.BASE_DIR, settings.PERMISSIONS_JSON))

    def _create_default_admin(self):

        if not User.objects.filter(username=settings.ADMIN_USERNAME).exists():
            self.logger.info('Could not find admin user \'{}\' user. Creating now...'.format(settings.ADMIN_USERNAME))
            admin = User.objects.create_user(username=settings.ADMIN_USERNAME,
                                             password=settings.ADMIN_PASSWORD,
                                             email=settings.ADMIN_EMAIL)

            admin.is_staff = True
            admin.is_superuser = True

            admin_group = Group.objects.get_or_create(name='admin')[0]
            admin_group.save()

            admin_group.user_set.add(admin)
            admin_group.save()

            self.logger.warning('\'{} \' password is \'{}\''.format(settings.ADMIN_USERNAME, settings.ADMIN_PASSWORD))
            self.logger.warning('⚠️⚠️⚠️ THIS SHOULD BE CHANGED IMMEDIATELY ⚠️⚠️⚠️')

        else:
            self.logger.info('Found \'admin\' user.')

    def __init__(self, get_response):
        self.get_response = get_response
        self.logger = logging.getLogger('AccessPolicyMiddleware')

        if settings.ENV_NAME == 'wild_west':
            self.logger.warning('⚠️🌵️🐎 WILD WEST MODE 🐎🌵️⚠️️')
            self.logger.warning(
                'WILD WEST MODE WILL PURGE ALL PERMISSIONS FROM YOUR DATABASE. YOU WILL NEED TO REBUILD THE DATABASE '
                'PERMISSIONS AFTER THIS RUN. DO NOT RUN IN PRODUCTION'
            )
            self.logger.warning('⚠️🌵️🐎 WILD WEST MODE 🐎🌵️⚠️️')
            # self.logger.warning(
            #     '⚠️🌵️🐎 WILD WEST MODE 🐎🌵️⚠️️ -  Loading wild west authorization models')
            self._load_wild_west_access_policies()
        else:
            print('Loading default authorization models...')
            self._load_default_access_policies()

        self._create_default_admin()

    def __call__(self, request):
        return self.get_response(request)

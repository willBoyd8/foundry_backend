import json
import logging
import os

from apscheduler.schedulers.background import BackgroundScheduler
from django.conf import settings
from django.contrib.auth.models import User, Group
from django_apscheduler.jobstores import register_events

from foundry_backend.api.nightly.daily_messages import gather_daily_views
from foundry_backend.api.models import IAMPolicy
from foundry_backend.api.serializers import IAMPolicySerializer

scheduler = BackgroundScheduler(settings.SCHEDULER_CONFIG)


def start_nightly_tasks(logger: logging.Logger):
    logger.info('Registering tasks...')

    logger.info('Registering task: \'gather_daily_views\'')
    scheduler.add_job(
        gather_daily_views,
        'cron',
        id='gather_daily_view',
        hour=settings.DAILY_MESSAGE_TIME['HOUR'],
        minute=settings.DAILY_MESSAGE_TIME['MINUTE'],
        second=settings.DAILY_MESSAGE_TIME['SECOND'],
        replace_existing=True,
        kwargs={'logger': logger}
    )
    logger.info('Done registering tasks: \'gather_daily_views\'')

    register_events(scheduler)

    scheduler.start()


def load_iam_policies(logger: logging.Logger):
    def _load_json_access_policies(path: str):
        logger.info('Deleting default authentication model...')

        IAMPolicy.objects.filter(name='default').delete()

        logger.info('Creating authentication models')

        with open(path, 'r') as permissions_file:
            permissions_data = json.loads(str(permissions_file.read()))
            for perm in permissions_data:
                serializer = IAMPolicySerializer(data=perm)

                if serializer.is_valid():
                    logger.info('Saving Policy: \'{}\''.format(perm['name']))
                    serializer.save()

    def _load_default_access_policies():
        _load_json_access_policies(os.path.join(settings.BASE_DIR, settings.PERMISSIONS_JSON))

    def _load_wild_west_access_policies():
        IAMPolicy.objects.all().delete()

        _load_json_access_policies(os.path.join(settings.BASE_DIR, settings.PERMISSIONS_JSON))

    def _create_default_admin():
        if not User.objects.filter(username=settings.ADMIN_USERNAME).exists():
            logger.info('Could not find admin user \'{}\' user. Creating now...'.format(settings.ADMIN_USERNAME))
            admin = User.objects.create_user(username=settings.ADMIN_USERNAME,
                                             password=settings.ADMIN_PASSWORD,
                                             email=settings.ADMIN_EMAIL)

            admin.is_staff = True
            admin.is_superuser = True

            admin_group = Group.objects.get_or_create(name='admin')[0]
            admin_group.save()

            admin_group.user_set.add(admin)
            admin_group.save()

            logger.warning('\'{}\' password is \'{}\''.format(settings.ADMIN_USERNAME, settings.ADMIN_PASSWORD))
            logger.warning('⚠️⚠️⚠️ THIS SHOULD BE CHANGED IMMEDIATELY ⚠️⚠️⚠️')
        else:
            logger.info('Found \'admin\' user.')

    logger.info('Loading authentication policies...')

    if settings.ENV_NAME == 'wild_west':
        logger.warning(
            '⚠️🌵️🐎 WILD WEST MODE 🐎🌵️⚠️️'
            'WILD WEST MODE WILL PURGE ALL'
            'PERMISSIONS FROM YOUR DATABASE.'
            'YOU WILL NEED TO REBUILD THE '
            'DATABASE PERMISSIONS AFTER THIS'
            'RUN. DO NOT RUN IN PRODUCTION'
            '⚠️🌵️🐎 WILD WEST MODE 🐎🌵️⚠️️'
        )
        _load_wild_west_access_policies()

    else:
        _load_default_access_policies()

    _create_default_admin()

    logger.info('Done loading authentication policies.')

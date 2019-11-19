from django.core.exceptions import MiddlewareNotUsed

from . import daily_messages

import logging
from apscheduler.schedulers.background import BackgroundScheduler
from django.conf import settings


class ScheduleBatchTasksMiddleware:
    def __init__(self, get_response):
        self.get_response = get_response
        self.logger = logging.getLogger('ScheduleBatchTasksMiddleware')

        self.logger.info('Registering tasks...')

        self.logger.info('Registering task: \'gather_daily_views\'')
        scheduler = BackgroundScheduler(timezone=settings.TIME_ZONE)

        scheduler.add_job(daily_messages.gather_daily_views,
                          'cron',
                          hour=settings.DAILY_MESSAGE_TIME['HOUR'],
                          minute=settings.DAILY_MESSAGE_TIME['MINUTE'],
                          second=settings.DAILY_MESSAGE_TIME['SECOND'])
        scheduler.start()

        self.logger.info('Done!')

        raise MiddlewareNotUsed('Done initializing ScheduleBatchTasksMiddleware')

    def __call__(self, request):
        return self.get_response(request)

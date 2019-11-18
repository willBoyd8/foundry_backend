import datetime
import logging

import pytz
from django.conf import settings

from foundry_backend.database import models

daily_views_logger = logging.getLogger('daily_views')


def gather_daily_views():
    daily_views_logger.info('Logging daily views...')

    local_timezone = pytz.timezone(settings.TIME_ZONE)

    today_min = local_timezone.localize(datetime.datetime.combine(datetime.date.today(), datetime.time.min))
    today_max = local_timezone.localize(datetime.datetime.combine(datetime.date.today(), datetime.time.max))

    mls_numbers = models.MLSNumber.objects.all()

    for number in mls_numbers:
        listings = models.Listing.objects.filter(agent=number)

        for listing in listings:
            hits = listing.hits.filter(access_time__range=(today_min, today_max)).count()

            message_string = 'On {}, the listing {} was viewed {} times'.format(
                '{}/{}/{}'.format(today_min.month, today_min.day, today_min.year),
                '{} {}'.format(listing.property.address.street_number, listing.property.address.street),
                hits
            )

            message = models.UserMessage.objects.create(type='HITS', message=message_string, user_id=number.user.id)
            message.save()

    daily_views_logger.info('Done!')

import logging

from foundry_backend.database import models


def is_agent_in_agency(request, view, _) -> bool:
    agency: models.Agency = view.get_object()
    return agency.mls_numbers.filter(user_id=request.user.id).exists()


def realtor_owns_listing(request, view, _) -> bool:
    logger = logging.getLogger('access')

    logger.debug('Evaluating \'realtor_owns_listing\' condition...')

    if view.get_object().agent.id == request.user.mls_number.id:
        logger.debug('Success! User is owner')
        return True

    logger.debug('Failure! User is not owner')
    return False


def property_belongs_to_agency(request, view, _) -> bool:
    logger = logging.getLogger('access')

    logger.debug('Using \'property_belongs_to_agency\'')

    if isinstance(view.get_object(), models.Listing):
        listing: models.Listing = view.get_object()
        return listing.agent.agency.mls_numbers.filter(user_id=request.user.id).exists()
    elif isinstance(view.get_object(), models.Property):
        prop: models.Property = view.get_object()
        return prop.listing.agent.agency.mls_numbers.filter(user_id=request.user.id).exists()
    elif True in [isinstance(view.get_object(), obj) for obj in [models.HomeAlarm, models.Room]]:
        obj = view.get_object()
        return obj.property.listing.agent.agency.mls_numbers.filter(user_id=request.user.id).exists()
    elif isinstance(view.get_object(), models.Showing):
        showing: models.Showing = view.get_object()
        return showing.listing.agent.agency.mls_numbers.filter(user_id=request.user.id).exists()

    return True


def can_modify_showing(request, view, _) -> bool:
    logger = logging.getLogger('access')

    logger.debug('Using \'can_modify_showing\'')

    showing: models.Showing = view.get_object()

    return showing.listing.agent.agency.mls_numbers.filter(user_id=request.user.id).exists() or \
        showing.agent.agency.mls_numbers.filter(user_id=request.user.id).exists()

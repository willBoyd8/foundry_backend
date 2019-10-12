from foundry_backend.database import models


def is_agent_in_agency(request, view, _) -> bool:
    agency: models.Agency = view.get_object()
    return agency.mlsnumber_set.filter(user_id=request.user.id).exists()


def property_belongs_to_agency(request, view, _) -> bool:
    if type(view.get_object()) == models.Listing:
        listing: models.Listing = view.get_object()
        return listing.agent.agency.mlsnumber_set.filter(user_id=request.user.id).exists()
    elif type(view.get_object()) == models.Property:
        prop: models.Property = view.get_object()
        return prop.listing.agent.agency.mlsnumber_set.filter(user_id=request.user.id).exists()
    elif type(view.get_object()) in [models.HomeAlarm, models.Room]:
        obj = view.get_object()
        return obj.property.listing.agent.agency.mlsnumber_set.filter(user_id=request.user.id).exists()

    return False

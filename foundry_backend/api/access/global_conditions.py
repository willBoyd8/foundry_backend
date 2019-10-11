from foundry_backend.database import models


def is_agent_in_agency(request, view, _) -> bool:
    agency: models.Agency = view.get_object()
    return agency.mlsnumber_set.filter(user_id=request.user.id).exists()

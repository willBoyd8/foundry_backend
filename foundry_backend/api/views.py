from foundry_backend.database import models as db_models
from rest_framework import viewsets
from . import serializers


# Create your views here.
class AgencyViewSet(viewsets.ModelViewSet):
    """
    API Endpoint for Foundry Agencies
    """
    queryset = db_models.Agency.objects.all()
    serializer_class = serializers.AgencySerializer
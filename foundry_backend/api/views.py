from foundry_backend.database import models as db_models
from rest_framework import viewsets
from . import serializers


class UserViewSet(viewsets.ModelViewSet):
    """
    API Endpoint for user creation and management
    """
    queryset = db_models.User.objects.all()
    serializer_class = serializers.UserSerializer


class AgencyViewSet(viewsets.ModelViewSet):
    """
    API Endpoint for Foundry Agencies
    """
    queryset = db_models.Agency.objects.all()
    serializer_class = serializers.AgencySerializer


class MLSNumberViewSet(viewsets.ModelViewSet):
    """
    API Endpoint for Foundry Agencies
    """
    queryset = db_models.MLSNumber.objects.all()
    serializer_class = serializers.MLSNumberSerializer


class RealtorUserViewSet(viewsets.ModelViewSet):
    """
    API Endpoint for Foundry Agencies
    """
    queryset = db_models.Realtor.objects.all()
    serializer_class = serializers.RealtorUserSerializer


class ListingViewSet(viewsets.ModelViewSet):
    """
    API Endpoint for listings
    """
    queryset = db_models.Listing.objects.all()
    serializer_class = serializers.ListingSerializer

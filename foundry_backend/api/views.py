from foundry_backend.database import models as db_models
from rest_framework import viewsets
from . import serializers
from dry_rest_permissions.generics import DRYPermissions


class AgencyViewSet(viewsets.ModelViewSet):
    """
    API Endpoint for Foundry Agencies
    """
    permission_classes = (DRYPermissions,)
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


class NearbyAttractionViewSet(viewsets.ModelViewSet):
    """
    API Endpoint for Subdivisions
    """
    permission_classes = (DRYPermissions,)
    queryset = db_models.NearbyAttraction.objects.all()
    serializer_class = serializers.NearbyAttractionSerializer


class PropertyViewSet(viewsets.ModelViewSet):
    """
    API Endpoint for Properties
    """
    permission_classes = (DRYPermissions,)
    queryset = db_models.Property.objects.all()
    serializer_class = serializers.PropertySerializer


class NearbyAttractionPropertyConnectorViewSet(viewsets.ModelViewSet):
    """
    API Endpoint for NearbyAttractionPropertyConnectors
    """
    permission_classes = (DRYPermissions,)
    queryset = db_models.NearbyAttractionPropertyConnector.objects.all()
    serializer_class = serializers.NearbyAttractionPropertyConnectorSerializer


class ListingViewSet(viewsets.ModelViewSet):
    """
    API Endpoint for listings
    """
    queryset = db_models.Listing.objects.all()
    serializer_class = serializers.ListingSerializer


class RoomViewSet(viewsets.ModelViewSet):
    """
    API Endpoint for listings
    """
    queryset = db_models.Listing.objects.all()
    serializer_class = serializers.RoomSerializer

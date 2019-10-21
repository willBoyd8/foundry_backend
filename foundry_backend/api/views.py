from foundry_backend.api import models
from foundry_backend.database import models as db_models
from rest_framework import viewsets
from . import serializers
from .access import make_access_policy
from .access import APIAccessPolicyBase
from . import access


class AgencyViewSet(viewsets.ModelViewSet):
    """
    API Endpoint for Foundry Agencies
    """
    permission_classes = (make_access_policy('Agency', 'agency-access-policy'),)

    @property
    def access_policy(self):
        return self.permission_classes[0]

    queryset = db_models.Agency.objects.all()
    serializer_class = serializers.AgencySerializer


class MLSNumberViewSet(viewsets.ModelViewSet):
    """
    API Endpoint for Foundry Agencies
    """
    permission_classes = (make_access_policy('MLSNumber', 'mls-number-access-policy'),)

    @property
    def access_policy(self):
        return self.permission_classes[0]

    queryset = db_models.MLSNumber.objects.all()
    serializer_class = serializers.MLSNumberSerializer


class NearbyAttractionViewSet(viewsets.ModelViewSet):
    """
    API Endpoint for Subdivisions
    """
    permission_classes = (make_access_policy('RealtorAdmin', 'realtor-admin-access-policy'),)

    @property
    def access_policy(self):
        return self.permission_classes[0]

    queryset = db_models.NearbyAttraction.objects.all()
    serializer_class = serializers.NearbyAttractionSerializer


class PropertyViewSet(viewsets.ModelViewSet):
    """
    API Endpoint for Properties
    """
    permission_classes = (make_access_policy('Property', 'inter-agency-listing-access-policy'),)

    @property
    def access_policy(self):
        return self.permission_classes[0]

    queryset = db_models.Property.objects.all()
    serializer_class = serializers.PropertySerializer


class NearbyAttractionPropertyConnectorViewSet(viewsets.ModelViewSet):
    """
    API Endpoint for NearbyAttractionPropertyConnectors
    """
    permission_classes = (make_access_policy('RealtorAdmin', 'realtor-admin-access-policy'),)

    @property
    def access_policy(self):
        return self.permission_classes[0]

    queryset = db_models.NearbyAttractionPropertyConnector.objects.all()
    serializer_class = serializers.NearbyAttractionPropertyConnectorSerializer


class ListingViewSet(viewsets.ModelViewSet):
    """
    API Endpoint for listings
    """
    permission_classes = (make_access_policy('InterAgencyListing', 'inter-agency-listing-access-policy'),)

    @property
    def access_policy(self):
        return self.permission_classes[0]

    queryset = db_models.Listing.objects.all()
    serializer_class = serializers.ListingSerializer


class RoomViewSet(viewsets.ModelViewSet):
    """
    API Endpoint for listings
    """
    queryset = db_models.Listing.objects.all()
    serializer_class = serializers.RoomSerializer


class HomeAlarmViewSet(viewsets.ModelViewSet):
    """
    API Endpoint for home alarms
    """
    permission_classes = (make_access_policy('HomeAlarm', 'home-alarm-access-policy'),)

    @property
    def access_policy(self):
        return self.permission_classes[0]

    queryset = db_models.Listing.objects.all()
    serializer_class = serializers.HomeAlarmSerializer


class ShowingViewSet(viewsets.ModelViewSet):
    """
    API Endpoint for home alarms
    """
    # TODO: Change me
    permission_classes = (make_access_policy('HomeAlarm', 'home-alarm-access-policy'),)

    @property
    def access_policy(self):
        return self.permission_classes[0]

    queryset = db_models.Listing.objects.all()
    serializer_class = serializers.HomeAlarmSerializer


class IAMPolicyViewSet(viewsets.ModelViewSet):
    """
    API Endpoint for IAM Lists
    """
    permission_classes = (make_access_policy('IAMPolicy', 'iam-policy-access-policy'),)

    @property
    def access_policy(self):
        return self.permission_classes[0]

    queryset = models.IAMPolicy.objects.all()
    serializer_class = serializers.IAMPolicySerializer

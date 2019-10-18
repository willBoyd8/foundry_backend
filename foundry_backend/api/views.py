from foundry_backend.api import models
from foundry_backend.database import models as db_models
from rest_framework import viewsets
from . import serializers
from . import access


class AgencyViewSet(viewsets.ModelViewSet):
    """
    API Endpoint for Foundry Agencies
    """
    permission_classes = (access.AgencyAccessPolicy,)

    @property
    def access_policy(self):
        return self.permission_classes[0]

    queryset = db_models.Agency.objects.all()
    serializer_class = serializers.AgencySerializer


class MLSNumberViewSet(viewsets.ModelViewSet):
    """
    API Endpoint for Foundry Agencies
    """
    permission_classes = (access.MLSNumberAccessPolicy,)

    @property
    def access_policy(self):
        return self.permission_classes[0]

    queryset = db_models.MLSNumber.objects.all()
    serializer_class = serializers.MLSNumberSerializer


class NearbyAttractionViewSet(viewsets.ModelViewSet):
    """
    API Endpoint for Subdivisions
    """
    permission_classes = (access.RealtorAdminAccessPolicy,)

    @property
    def access_policy(self):
        return self.permission_classes[0]

    queryset = db_models.NearbyAttraction.objects.all()
    serializer_class = serializers.NearbyAttractionSerializer


class PropertyViewSet(viewsets.ModelViewSet):
    """
    API Endpoint for Properties
    """
    permission_classes = (access.InterAgencyListingAccessPolicy,)

    @property
    def access_policy(self):
        return self.permission_classes[0]

    queryset = db_models.Property.objects.all()
    serializer_class = serializers.PropertySerializer


class NearbyAttractionPropertyConnectorViewSet(viewsets.ModelViewSet):
    """
    API Endpoint for NearbyAttractionPropertyConnectors
    """
    permission_classes = (access.RealtorAdminAccessPolicy,)

    @property
    def access_policy(self):
        return self.permission_classes[0]

    queryset = db_models.NearbyAttractionPropertyConnector.objects.all()
    serializer_class = serializers.NearbyAttractionPropertyConnectorSerializer


class ListingViewSet(viewsets.ModelViewSet):
    """
    API Endpoint for listings
    """
    permission_classes = (access.InterAgencyListingAccessPolicy,)

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
    permission_classes = (access.HomeAlarmAccessPolicy,)

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
    permission_classes = (access.HomeAlarmAccessPolicy,)

    @property
    def access_policy(self):
        return self.permission_classes[0]

    queryset = db_models.Listing.objects.all()
    serializer_class = serializers.HomeAlarmSerializer


class IAMPolicyRuleViewSet(viewsets.ModelViewSet):
    """
    API Endpoint for IAM Policies
    """
    queryset = models.IAMPolicyRule.objects.all()
    serializer_class = serializers.IAMPolicyRuleSerializer


class IAMPolicyViewSet(viewsets.ModelViewSet):
    """
    API Endpoint for IAM Lists
    """
    queryset = models.IAMPolicy.objects.all()
    serializer_class = serializers.IAMPolicySerializer

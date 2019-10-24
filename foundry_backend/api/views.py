from rest_framework.exceptions import ValidationError
from foundry_backend.api import models
from foundry_backend.database import models as db_models
from rest_framework import viewsets

from foundry_backend.database.models import MLSNumber
from . import serializers
from .access import make_access_policy


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

    def get_queryset(self):
        if self.kwargs.get('agency_pk') is not None:
            return MLSNumber.objects.filter(agency=self.kwargs['agency_pk'])

    def perform_create(self, serializer: serializers.MLSNumberSerializer):
        serializer = serializers.FullMLSNumberSerializer(data={**serializer.data, 'agency': self.kwargs['agency_pk']})

        if serializer.is_valid():
            serializer.save()
        else:
            raise ValidationError(serializer.errors)

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
    permission_classes = (make_access_policy('Showing', 'showing-access-policy'),)

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


class IAMPolicyStatementViewSet(viewsets.ModelViewSet):
    permission_classes = (make_access_policy('IAMPolicy', 'iam-policy-access-policy'),)

    @property
    def access_policy(self):
        return self.permission_classes[0]

    queryset = models.IAMPolicyStatement.objects.all()
    serializer_class = serializers.IAMPolicyStatementSerializer

    def get_queryset(self):
        if self.kwargs.get('policy_pk') is not None:
            return models.IAMPolicyStatement.objects.filter(policy=self.kwargs['policy_pk'])

    def perform_create(self, serializer: serializers.IAMPolicyStatementSerializer):
        serializer = serializers.FullIAMPolicyStatementSerializer(data={**serializer.data,
                                                                        'policy': self.kwargs['policy_pk']})

        if serializer.is_valid():
            serializer.save()
        else:
            raise ValidationError(serializer.errors)


class IAMPolicyStatementPrincipalViewSet(viewsets.ModelViewSet):
    permission_classes = (make_access_policy('IAMPolicy', 'iam-policy-access-policy'),)

    @property
    def access_policy(self):
        return self.permission_classes[0]

    queryset = models.IAMPolicyStatementPrincipal.objects.all()
    serializer_class = serializers.IAMPolicyStatementPrincipalSerializer

    def get_queryset(self):
        if self.kwargs.get('rule_pk') is not None:
            return models.IAMPolicyStatementPrincipal.objects.filter(statement=self.kwargs['rule_pk'])

    def perform_create(self, serializer: serializers.IAMPolicyStatementPrincipalSerializer):
        serializer = serializers.FullIAMPolicyStatementPrincipalSerializer(data={**serializer.data,
                                                                                 'statement': self.kwargs['rule_pk']})

        if serializer.is_valid():
            serializer.save()
        else:
            raise ValidationError(serializer.errors)


class IAMPolicyStatementConditionViewSet(viewsets.ModelViewSet):
    permission_classes = (make_access_policy('IAMPolicy', 'iam-policy-access-policy'),)

    @property
    def access_policy(self):
        return self.permission_classes[0]

    queryset = models.IAMPolicyStatementCondition.objects.all()
    serializer_class = serializers.IAMPolicyStatementConditionSerializer

    def get_queryset(self):
        if self.kwargs.get('policy_pk') is not None:
            return models.IAMPolicyStatementCondition.objects.filter(policy=self.kwargs['policy_pk'])

    def perform_create(self, serializer: serializers.IAMPolicyStatementConditionSerializer):
        serializer = serializers.FullIAMPolicyStatementConditionSerializer(data={**serializer.data,
                                                                                 'rule': self.kwargs['rule_pk']})

        if serializer.is_valid():
            serializer.save()
        else:
            raise ValidationError(serializer.errors)


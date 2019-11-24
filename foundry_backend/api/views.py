from rest_framework.parsers import MultiPartParser, FormParser
from rest_framework.viewsets import GenericViewSet

from foundry_backend.api import models
from foundry_backend.api.filters import ListingFilterSet, AgencyFilterSet, ListingImageFilterSet, MLSNumberFilterSet, \
    ListingsHitFilterSet, ShowingReviewFilterSet
from foundry_backend.database import models as db_models
from rest_framework import viewsets, mixins
from foundry_backend.database.models import MLSNumber, Room, NearbyAttraction
from . import serializers
from .access import make_access_policy


class UserMessageViewSet(viewsets.ModelViewSet):
    """
    API Endpoint for user messages
    """
    permission_classes = (make_access_policy('UserMessage', 'user-message-access-policy'),)

    @property
    def access_policy(self):
        return self.permission_classes[0]

    def get_queryset(self):
        if self.request.user.is_authenticated:
            return self.request.user.messages.all()
        else:
            return []

    queryset = db_models.UserMessage.objects.all()
    serializer_class = serializers.UserMessageSerializer


class AvatarViewSet(viewsets.ModelViewSet):
    """
    API Endpoint for Avatars
    """
    parser_classes = (MultiPartParser, FormParser)
    permission_classes = (make_access_policy('Avatar', 'avatar-access-policy'),)

    @property
    def access_policy(self):
        return self.permission_classes[0]

    queryset = db_models.Avatar.objects.all()
    serializer_class = serializers.AvatarSerializer


class AgencyViewSet(viewsets.ModelViewSet):
    """
    API Endpoint for Foundry Agencies
    """
    permission_classes = (make_access_policy('Agency', 'agency-access-policy'),)

    @property
    def access_policy(self):
        return self.permission_classes[0]

    filterset_class = AgencyFilterSet

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

        return serializer.errors

    queryset = db_models.MLSNumber.objects.all()
    serializer_class = serializers.MLSNumberSerializer


class AllMLSNumbersViewSet(mixins.RetrieveModelMixin, mixins.ListModelMixin, viewsets.GenericViewSet):
    """
    API Endpoint for searching all the realtors
    """
    permission_classes = (make_access_policy('MLSNumber', 'mls-number-access-policy'),)

    @property
    def access_policy(self):
        return self.permission_classes[0]

    queryset = db_models.MLSNumber.objects.all()
    serializer_class = serializers.FullMLSNumberSerializer

    filterset_class = MLSNumberFilterSet


class NearbyAttractionViewSet(viewsets.ModelViewSet):
    """
    API Endpoint for Subdivisions
    """
    permission_classes = (make_access_policy('RealtorAdmin', 'realtor-admin-access-policy'),)

    @property
    def access_policy(self):
        return self.permission_classes[0]

    def get_queryset(self):
        if self.kwargs.get('property_pk') is not None:
            # return Listing.objects.filter(property=self.kwargs['property_pk'])
            return NearbyAttraction.objects.filter(property=self.kwargs['property_pk'])

    def perform_create(self, serializer: serializers.NearbyAttractionSerializer):
        serializer = serializers.FullNearbyAttractionSerializer(data={**serializer.data,
                                                                      'property': self.kwargs['property_pk']})

        if serializer.is_valid():
            serializer.save()

        return serializer.errors

    queryset = db_models.NearbyAttraction.objects.all()
    serializer_class = serializers.NearbyAttractionSerializer


class PropertyViewSet(viewsets.ModelViewSet):
    """
    API Endpoint for Properties
    """
    permission_classes = (make_access_policy('InterAgencyListing', 'inter-agency-listing-access-policy'),)

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

    filterset_class = ListingFilterSet

    queryset = db_models.Listing.objects.filter()
    serializer_class = serializers.ListingSerializer


class ListingsHitViewSet(mixins.CreateModelMixin, GenericViewSet):
    """
        API Endpoint for listings
        """
    permission_classes = (make_access_policy('ListingsHit', 'listings-hit-access-policy'),)

    @property
    def access_policy(self):
        return self.permission_classes[0]

    filterset_class = ListingsHitFilterSet

    queryset = db_models.ListingsHit.objects.all()
    serializer_class = serializers.ListingsHitSerializer


class ListingImageViewSet(viewsets.ModelViewSet):
    """
    API Endpoint for listing images
    """
    parser_classes = (MultiPartParser, FormParser)
    permission_classes = (make_access_policy('InterAgencyListing', 'inter-agency-listing-access-policy'),)

    @property
    def access_policy(self):
        return self.permission_classes[0]

    filterset_class = ListingImageFilterSet

    serializer_class = serializers.ListingImageSerializer
    queryset = db_models.ListingImage.objects.all()


class RoomViewSet(viewsets.ModelViewSet):
    """
    API Endpoint for listings
    """
    queryset = db_models.Listing.objects.all()
    serializer_class = serializers.RoomSerializer

    def get_queryset(self):
        if self.kwargs.get('property_pk') is not None:
            return Room.objects.filter(property=self.kwargs['property_pk'])

    def perform_create(self, serializer: serializers.RoomSerializer):
        serializer = serializers.FullRoomSerializer(data={**serializer.data, 'property': self.kwargs['property_pk']})

        if serializer.is_valid():
            serializer.save()

        return serializer.errors


class HomeAlarmViewSet(mixins.CreateModelMixin,
                       mixins.RetrieveModelMixin,
                       mixins.UpdateModelMixin,
                       viewsets.GenericViewSet):
    """
    retrieve:
        Returns the property's home alarm

    partial_update:
        Partially update the property's alarm listing

    update:
        Update the property's alarm listing
    """
    permission_classes = (make_access_policy('HomeAlarm', 'home-alarm-access-policy'),)

    @property
    def access_policy(self):
        return self.permission_classes[0]

    queryset = db_models.HomeAlarm.objects.all()
    serializer_class = serializers.HomeAlarmSerializer


class ShowingViewSet(viewsets.ModelViewSet):
    """
    API Endpoint for home alarms
    """
    permission_classes = (make_access_policy('Showing', 'showing-access-policy'),)

    @property
    def access_policy(self):
        return self.permission_classes[0]

    queryset = db_models.Showing.objects.all()
    serializer_class = serializers.ShowingSerializer

    def perform_create(self, serializer: serializers.ShowingSerializer):
        serializer = serializers.FullShowingSerializer(data={**serializer.data, 'listing': self.kwargs['listing_pk']})

        if serializer.is_valid():
            serializer.save()

        return serializer.errors


class ShowingReviewViewSet(viewsets.ModelViewSet):
    """
    API Endpoint for Showing Surveys
    """
    permission_classes = (make_access_policy('ShowingReview', 'showing-review-access-policy'),)

    @property
    def access_policy(self):
        return self.permission_classes[0]

    filterset_class = ShowingReviewFilterSet

    queryset = db_models.ShowingReview.objects.all()
    serializer_class = serializers.ShowingReviewSerializer


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

        return serializer.errors


class IAMPolicyStatementPrincipalViewSet(viewsets.ModelViewSet):
    permission_classes = (make_access_policy('IAMPolicy', 'iam-policy-access-policy'),)

    @property
    def access_policy(self):
        return self.permission_classes[0]

    queryset = models.IAMPolicyStatementPrincipal.objects.all()
    serializer_class = serializers.IAMPolicyStatementPrincipalSerializer

    def get_queryset(self):
        if self.kwargs.get('statement_pk') is not None:
            return models.IAMPolicyStatementPrincipal.objects.filter(statement=self.kwargs['statement_pk'])

    def perform_create(self, serializer: serializers.IAMPolicyStatementPrincipalSerializer):
        serializer = serializers.FullIAMPolicyStatementPrincipalSerializer(data={**serializer.data,
                                                                                 'statement': self.kwargs['statement_pk']})

        if serializer.is_valid():
            serializer.save()

        return serializer.errors


class IAMPolicyStatementConditionViewSet(viewsets.ModelViewSet):
    permission_classes = (make_access_policy('IAMPolicy', 'iam-policy-access-policy'),)

    @property
    def access_policy(self):
        return self.permission_classes[0]

    queryset = models.IAMPolicyStatementCondition.objects.all()
    serializer_class = serializers.IAMPolicyStatementConditionSerializer

    def get_queryset(self):
        if self.kwargs.get('statement_pk') is not None:
            return models.IAMPolicyStatementCondition.objects.filter(statement=self.kwargs['statement_pk'])

    def perform_create(self, serializer: serializers.IAMPolicyStatementConditionSerializer):
        serializer = serializers.FullIAMPolicyStatementConditionSerializer(
            data={
                **serializer.data,
                'statement': self.kwargs['statement_pk']
            }
        )

        if serializer.is_valid():
            serializer.save()

        return serializer.errors

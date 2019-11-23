from django.contrib.auth.models import User
from djoser.serializers import UserCreateSerializer
from drf_writable_nested import WritableNestedModelSerializer
from rest_framework.exceptions import ValidationError
from rest_framework.fields import MultipleChoiceField
from foundry_backend.api import models
from foundry_backend.database import models as db_models
from rest_framework import serializers


class UserMessageSerializer(serializers.ModelSerializer):
    class Meta:
        model = db_models.UserMessage
        fields = '__all__'


class AvatarSerializer(serializers.ModelSerializer):
    class Meta:
        model = db_models.Avatar
        fields = '__all__'


class AddressSerializer(serializers.ModelSerializer):
    class Meta:
        model = db_models.Address
        fields = ['street_number', 'street', 'locality', 'postal_code', 'state', 'state_code']


class FullMLSNumberSerializer(serializers.ModelSerializer):
    class Meta:
        model = db_models.MLSNumber
        fields = '__all__'
        read_only_fields = ('number',)


class UserInfoSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ['username', 'email', 'first_name', 'last_name']


class UserRegistrationSerializer(UserCreateSerializer):
    class Meta(UserCreateSerializer.Meta):
        fields = ('url', 'id', 'email', 'username', 'first_name', 'last_name', 'password',)


class MLSNumberSerializer(serializers.ModelSerializer):
    user_info = UserInfoSerializer(many=False, read_only=True, source='user')

    class Meta:
        model = db_models.MLSNumber
        fields = ['id', 'number', 'user', 'user_info']
        read_only_fields = ('number',)


class AgencySerializer(WritableNestedModelSerializer):
    address = AddressSerializer()
    mls_numbers = MLSNumberSerializer(many=True)

    class Meta:
        model = db_models.Agency
        fields = ['id', 'name', 'address', 'phone', 'mls_numbers']


class FullNearbyAttractionSerializer(serializers.ModelSerializer):
    class Meta:
        model = db_models.NearbyAttraction
        fields = '__all__'


class NearbyAttractionSerializer(serializers.ModelSerializer):
    class Meta:
        model = db_models.NearbyAttraction
        fields = ['id', 'name', 'type']


class FullRoomSerializer(serializers.ModelSerializer):
    class Meta:
        model = db_models.Room
        fields = '__all__'


class RoomSerializer(serializers.ModelSerializer):
    class Meta:
        model = db_models.Room
        fields = ['id', 'description', 'name', 'type']


class FullHomeAlarmSerializer(serializers.ModelSerializer):
    class Meta:
        model = db_models.HomeAlarm
        fields = '__all__'


class HomeAlarmSerializer(serializers.ModelSerializer):
    class Meta:
        model = db_models.HomeAlarm
        fields = ['id', 'arm_code', 'disarm_code', 'password', 'notes']


class FullPropertySerializer(WritableNestedModelSerializer):
    address = AddressSerializer()
    rooms = RoomSerializer(many=True)
    nearby_attractions = NearbyAttractionSerializer(many=True)
    home_alarm = HomeAlarmSerializer(write_only=True)

    class Meta:
        model = db_models.Property
        fields = [
            'id',
            'property',
            'address',
            'square_footage',
            'acreage',
            'type',
            'rooms',
            'nearby_attractions',
            'home_alarm'
        ]


class PropertySerializer(WritableNestedModelSerializer):
    address = AddressSerializer()
    rooms = RoomSerializer(many=True)
    nearby_attractions = NearbyAttractionSerializer(many=True)
    home_alarm = HomeAlarmSerializer(write_only=True)

    @staticmethod
    def validate_rooms(value):
        room_names = [v['name'] for v in value]

        if len(room_names) is not len(set(room_names)):
            raise ValidationError('Room names must be unique')

        return value

    @staticmethod
    def validate_nearby_attractions(value):
        attraction_names = [v['name'] for v in value]

        if len(attraction_names) is not len(set(attraction_names)):
            raise ValidationError('Nearby Attraction names must be unique')

        return value

    class Meta:
        model = db_models.Property
        fields = [
            'id',
            'address',
            'square_footage',
            'acreage',
            'type',
            'rooms',
            'nearby_attractions',
            'home_alarm'
        ]
        
        extra_kwargs = {
            'home_alarm': {'write_only': True}
        }


class NearbyAttractionPropertyConnectorSerializer(serializers.ModelSerializer):
    class Meta:
        model = db_models.NearbyAttractionPropertyConnector
        fields = ['id', 'attraction', 'property']


class ListingSerializer(WritableNestedModelSerializer):
    property = PropertySerializer(many=False)

    class Meta:
        model = db_models.Listing
        fields = '__all__'


class ListingsHitSerializer(serializers.ModelSerializer):
    class Meta:
        model = db_models.ListingsHit
        fields = '__all__'
        read_only_fields = ['access_time']


class ListingImageSerializer(serializers.ModelSerializer):
    class Meta:
        model = db_models.ListingImage
        fields = '__all__'


class FullShowingSerializer(serializers.ModelSerializer):
    class Meta:
        model = db_models.Showing
        fields = '__all__'


class ShowingSerializer(serializers.ModelSerializer):
    class Meta:
        model = db_models.Showing
        fields = ['id', 'agent', 'end_time', 'start_time']


class ShowingReviewSerializer(serializers.ModelSerializer):
    class Meta:
        model = db_models.ShowingReview
        fields = '__all__'


class SalesContractSerializer(serializers.Serializer):
    address = serializers.CharField()
    selling_agency = serializers.CharField()
    selling_agent = serializers.CharField()
    buyer_name = serializers.CharField()
    price = serializers.CharField()
    deposit = serializers.CharField()
    closing_date = serializers.CharField()


class RequestForRepairsSerializer(serializers.Serializer):
    requester = serializers.CharField()
    contact_number = serializers.CharField()
    address = serializers.CharField()
    facilitating_agent = serializers.CharField()
    description = serializers.CharField()


class EnableRealtorSerializer(serializers.Serializer):
    mls_number = serializers.CharField(max_length=15, help_text="The MLS Number for the realtor being registered")
    user = serializers.IntegerField(help_text="The user to associate as a realtor")


class EnableAdminSerializer(serializers.Serializer):
    user = serializers.IntegerField(help_text="The user to associate as an admin")


class FullIAMPolicyStatementPrincipalSerializer(serializers.ModelSerializer):
    """
    Serialize an IAMPolicyRulePrincipal item
    """
    class Meta:
        model = models.IAMPolicyStatementPrincipal
        fields = '__all__'


class IAMPolicyStatementPrincipalSerializer(serializers.ModelSerializer):
    """
    Serialize an IAMPolicyStatement item
    """
    class Meta:
        model = models.IAMPolicyStatementPrincipal
        fields = ['id', 'value']


class FullIAMPolicyStatementConditionSerializer(serializers.ModelSerializer):
    """
    Serialize an IAMPolicyPolicyCondition item
    """
    class Meta:
        model = models.IAMPolicyStatementCondition
        fields = '__all__'


class IAMPolicyStatementConditionSerializer(serializers.ModelSerializer):
    """
    Serialize an IAMPolicyStatementConditionPrincipal item
    """
    class Meta:
        model = models.IAMPolicyStatementCondition
        fields = ['id', 'value']


class IAMPolicyStatementSerializer(WritableNestedModelSerializer):
    """
    Serialize an IAMPolicyStatement
    """
    actions = MultipleChoiceField(choices=models.IAMPolicyStatement.STATEMENT_ACTION_OPTIONS)
    principals = IAMPolicyStatementPrincipalSerializer(many=True)
    conditions = IAMPolicyStatementConditionSerializer(many=True)

    class Meta:
        model = models.IAMPolicyStatement
        fields = ['id', 'notes', 'actions', 'effect', 'principals', 'conditions']


class FullIAMPolicyStatementSerializer(WritableNestedModelSerializer):
    """
    Serialize an IAMPolicyStatement
    """
    actions = MultipleChoiceField(choices=models.IAMPolicyStatement.STATEMENT_ACTION_OPTIONS)
    principals = IAMPolicyStatementPrincipalSerializer(many=True)
    conditions = IAMPolicyStatementConditionSerializer(many=True)

    class Meta:
        model = models.IAMPolicyStatement
        fields = '__all__'


class IAMPolicySerializer(WritableNestedModelSerializer):
    """
    Serialize an IAMPolicy
    """
    statements = IAMPolicyStatementSerializer(many=True)

    class Meta:
        model = models.IAMPolicy
        fields = ['id', 'name', 'notes', 'statements']

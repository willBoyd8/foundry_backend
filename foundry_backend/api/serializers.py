from drf_writable_nested import WritableNestedModelSerializer, NestedUpdateMixin
from rest_framework.fields import MultipleChoiceField
from foundry_backend.api import models
from foundry_backend.database import models as db_models
from rest_framework import serializers


class AddressSerializer(serializers.ModelSerializer):
    class Meta:
        model = db_models.Address
        fields = ['street_number', 'street', 'locality', 'postal_code', 'state', 'state_code']


class FullMLSNumberSerializer(serializers.ModelSerializer):
    class Meta:
        model = db_models.MLSNumber
        fields = '__all__'
        read_only_fields = ('number',)


class MLSNumberSerializer(serializers.ModelSerializer):
    class Meta:
        model = db_models.MLSNumber
        fields = ['id', 'number', 'user']
        read_only_fields = ('number',)


class AgencySerializer(WritableNestedModelSerializer):
    mls_numbers = MLSNumberSerializer(many=True)

    class Meta:
        model = db_models.Agency
        fields = ['id', 'name', 'address', 'phone', 'mls_numbers']


class NearbyAttractionSerializer(serializers.ModelSerializer):
    class Meta:
        model = db_models.NearbyAttraction
        fields = ['id', 'name', 'type']


class PropertySerializer(serializers.ModelSerializer):
    address = AddressSerializer()

    class Meta:
        model = db_models.Property
        fields = '__all__'

    def create(self, validated_data):
        address_data = validated_data.pop('address')
        address = db_models.Address.objects.create(**address_data)
        print(address)
        new_property = db_models.Property.objects.create(address_id=address.id,
                                                         square_footage=validated_data['square_footage'])
        return new_property


class NearbyAttractionPropertyConnectorSerializer(serializers.ModelSerializer):
    class Meta:
        model = db_models.NearbyAttractionPropertyConnector
        fields = ['id', 'attraction', 'property']


class ListingSerializer(serializers.ModelSerializer):
    class Meta:
        model = db_models.Listing
        fields = '__all__'


class RoomSerializer(serializers.ModelSerializer):
    class Meta:
        model = db_models.Room
        fields = '__all__'


class HomeAlarmSerializer(serializers.ModelSerializer):
    class Meta:
        model = db_models.HomeAlarm
        fields = '__all__'


class ShowingSerializer(serializers.ModelSerializer):
    class Meta:
        model = db_models.Showing
        fields = '__all__'


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

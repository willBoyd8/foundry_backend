from rest_framework.fields import MultipleChoiceField

from foundry_backend.api import models
from foundry_backend.database import models as db_models
from rest_framework import serializers


class AddressSerializer(serializers.ModelSerializer):
    class Meta:
        model = db_models.Address
        fields = ['street_number', 'street', 'locality', 'postal_code', 'state', 'state_code']


class AgencySerializer(serializers.ModelSerializer):
    class Meta:
        model = db_models.Agency
        fields = ['id', 'name', 'address', 'phone']


class MLSNumberSerializer(serializers.ModelSerializer):
    class Meta:
        model = db_models.MLSNumber
        fields = ['id', 'agency', 'number', 'user']
        read_only_fields = ('number',)


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


class IAMPolicyRuleSerializer(serializers.ModelSerializer):
    """
    Serialize an IAMPolicyRule
    """
    actions = MultipleChoiceField(choices=models.IAMPolicyRule.IAM_ACTION_OPTIONS)

    class Meta:
        model = models.IAMPolicyRule
        fields = ['id', 'notes', 'actions', 'effect']


class IAMPolicySerializer(serializers.ModelSerializer):
    """
    Serialize an IAMPolicy
    """
    rules = IAMPolicyRuleSerializer(many=True)

    class Meta:
        model = models.IAMPolicy
        fields = ['id', 'name', 'notes', 'rules']

    def create(self, validated_data):
        rules_data = validated_data.pop('rules')

        policy = models.IAMPolicy.objects.create(**validated_data)

        for rule_data in rules_data:
            IAMPolicyRuleSerializer().create({**rule_data, 'policy': policy})

        policy.save()
        return policy

    def update(self, instance, validated_data):
        # Get the rules JSON and the rule objects
        rules_data = validated_data.pop('rules')
        rules = list((instance.rules).all())

        # update the policy
        instance.notes = validated_data.get('notes', instance.notes)
        instance.name = validated_data.get('name', instance.name)
        instance.save()

        for rule_data in rules_data:
            # Remove and edit a rule
            rule = rules.pop(0)
            rule.notes = rule_data.get('notes', rule.notes)
            rule.actions = rule_data.get('actions', rule.actions)
            rule.effect = rule_data.get('effect', rule.effect)
            rule.save()

        return instance
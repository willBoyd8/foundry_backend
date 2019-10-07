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


class RealtorUserSerializer(serializers.ModelSerializer):
    class Meta:
        model = db_models.Realtor
        fields = ['id', 'mls', 'user']


class NearbyAttractionSerializer(serializers.ModelSerializer):
    class Meta:
        model = db_models.NearbyAttraction
        fields = ['id', 'name', 'type']


class PropertySerializer(serializers.ModelSerializer):
    address = AddressSerializer()

    class Meta:
        model = db_models.Property
        fields = ['id', 'address', 'square_footage']

    def create(self, validated_data):
        address_data = validated_data.pop('address')
        address = db_models.Address.objects.create(**address_data)
        print(address)
        new_property = db_models.Property.objects.create(address_id=address.id,
                                                         square_footage=validated_data['square_footage'],
                                                         description=validated_data['description'])
        return new_property


class NearbyAttractionPropertyConnectorSerializer(serializers.ModelSerializer):
    class Meta:
        model = db_models.NearbyAttractionPropertyConnector
        fields = ['id', 'attraction', 'property']


class ListingSerializer(serializers.ModelSerializer):
    class Meta:
        model = db_models.Listing
        fields = ['id', 'asking_price', 'description']


class RegisterRealtorSerializer(serializers.Serializer):
    def update(self, instance, validated_data):
        pass

    def create(self, validated_data):
        pass

    mls_number = serializers.CharField(max_length=15, help_text="The MLS Number for the realtor being registered")
    user = serializers.IntegerField(help_text="The user to associate as a realtor")


class RegisterAdminSerializer(serializers.Serializer):
    def update(self, instance, validated_data):
        pass

    def create(self, validated_data):
        pass

    user = serializers.IntegerField(help_text="The user to associate as an admin")

from foundry_backend.database import models as db_models
from rest_framework import serializers


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


class SubdivisionSerializer(serializers.ModelSerializer):
    class Meta:
        model = db_models.Subdivision
        fields = ['id', 'name']


class SchoolDistrictSerializer(serializers.ModelSerializer):
    class Meta:
        model = db_models.SchoolDistrict
        fields = ['id', 'name']


class ShoppingAreaSerializer(serializers.ModelSerializer):
    class Meta:
        model = db_models.ShoppingArea
        fields = ['id', 'name']


class PropertySerializer(serializers.ModelSerializer):
    class Meta:
        model = db_models.Property
        fields = ['id', 'address', 'square_footage', 'description', 'subdivision']


class ListingSerializer(serializers.ModelSerializer):
    class Meta:
        model = db_models.Listing
        fields = ['id', 'asking_price']


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

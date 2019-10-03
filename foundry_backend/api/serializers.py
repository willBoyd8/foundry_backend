from foundry_backend.database import models as db_models
from rest_framework import serializers


class AgencySerializer(serializers.ModelSerializer):
    class Meta:
        model = db_models.Agency
        fields = ['name', 'address', 'phone']


class MLSNumberSerializer(serializers.ModelSerializer):
    class Meta:
        model = db_models.MLSNumber
        fields = ['id', 'agency', 'number', 'user']
        read_only_fields = ('number',)


class RealtorUserSerializer(serializers.ModelSerializer):
    class Meta:
        model = db_models.Realtor
        fields = ['id', 'mls', 'user']


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

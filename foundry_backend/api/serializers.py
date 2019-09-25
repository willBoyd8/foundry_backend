from foundry_backend.database import models as db_models
from rest_framework import serializers


class AgencySerializer(serializers.HyperlinkedModelSerializer):
    class Meta:
        model = db_models.Agency
        fields = ['name', 'address', 'phone']

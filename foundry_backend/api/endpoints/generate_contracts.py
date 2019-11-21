from drf_yasg.utils import swagger_auto_schema
from rest_framework import views, status
from rest_framework.decorators import api_view
from rest_framework.request import Request
from rest_framework.response import Response

from foundry_backend.api import serializers


class GenerateSalesContract(views.APIView):
    serializers = serializers.SalesContractSerializer

    @staticmethod
    def get_serializer():
        return serializers.SalesContractSerializer()

    @staticmethod
    def post(request: Request, **kwargs):
        """
        Register a user as a realtor, using their MLS number
        """

        return Response({'information': 'make this a binary'}, status=status.HTTP_201_CREATED)

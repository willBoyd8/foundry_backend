import coreapi
import coreschema
from drf_yasg import views
from rest_framework.exceptions import NotFound, ValidationError
from rest_framework.request import Request
from rest_framework.response import Response
from rest_framework import status
from foundry_backend.api import serializers
from foundry_backend.database import models
from guardian.shortcuts import assign_perm


class RegisterRealtorView(views.APIView):
    serializers = serializers.RegisterRealtorSerializer

    @staticmethod
    def get_serializer():
        return serializers.RegisterRealtorSerializer()

    @staticmethod
    def post(request: Request, **kwargs):
        """
        Register a user as a realtor, using their MLS number
        """
        errors = {}
        serializer = serializers.RegisterRealtorSerializer(data=request.data)

        # check to see if we have any validation errors
        if not serializer.is_valid():
            errors = serializer.errors

        # check if the MLS number is in the database
        if not models.MLSNumber.objects.filter(number=request.data['mls_number']).exists():
            if not errors.get('mls_number'):
                errors['mls_number'] = []
            errors['mls_number'].append('The mls number given was not found')

        # check if we have a realtor already using this number
        if models.Realtor.objects.filter(mls__number=request.data['mls_number']).exists():
            if not errors.get('mls_number'):
                errors['mls_number'] = []
            errors['mls_number'].append('The mls number given is already registered')

        # check if we have a real user
        if not models.User.objects.filter(pk=request.data['user']).exists():
            if not errors.get('user'):
                errors['user'] = []
            errors['user'].append('no such user for pk "{}"'.format(request.data['user']))

        # If we have any errors, throw them now
        if len(errors) is not 0:
            raise ValidationError(errors)

        # create the realtor
        mls = models.MLSNumber.objects.filter(number=request.data['mls_number']).get()
        user = models.User.objects.filter(pk=request.data['user']).get()

        # Link the MLS Number to the User
        mls.owner = user
        mls.save()

        # Apply permissions to the user


        return Response({'id': mls.id}, status=status.HTTP_202_ACCEPTED)

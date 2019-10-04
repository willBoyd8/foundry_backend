import pytest
from django.test import TestCase


# Create your tests here.
from django.contrib.auth.models import Group, User
from requests import Response
from rest_framework import status
from rest_framework.utils import json


@pytest.mark.django_db
def test_agency_redirect(client):
    response = client.get('/api/v1/agencies')
    assert response.status_code == 301


@pytest.mark.django_db
def test_agency_permissions(client):
    # Test GET
    response: Response = client.get('/api/v1/agencies/')
    assert response.status_code == 200
    assert response.json() == []

    response: Response = client.post('/api/v1/agencies/', {'name': 'Realtors, Inc.',
                                                           'address': 'Someplace',
                                                           'phone': '202-555-0189'})
    assert response.status_code == status.HTTP_401_UNAUTHORIZED

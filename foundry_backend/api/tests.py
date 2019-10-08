import pytest
from django.contrib.auth.models import User
from requests import Response
from rest_framework import status
from rest_framework.test import force_authenticate
from foundry_backend.database.models import Realtor, MLSNumber
from . import views


@pytest.mark.django_db
def test_agency_redirect(client):
    response = client.get('/api/v1/agencies')
    assert response.status_code == 301


@pytest.mark.django_db
def test_agency_can_read(request_factory):
    request = request_factory.get('/api/v1/agencies/')
    view = views.AgencyViewSet.as_view({'get': 'list'})
    response = view(request)
    assert response.status_code == 200
    assert response.data == []


@pytest.mark.django_db
def test_unauthenticated_user_cannot_post_agency(request_factory):
    request: Response = request_factory.post('/api/v1/agencies/', {'name': 'Realtors, Inc.',
                                                                   'address': 'Someplace',
                                                                   'phone': '202-555-0189'})

    view = views.AgencyViewSet.as_view({'post': 'create'})
    response = view(request)

    assert response.status_code == status.HTTP_401_UNAUTHORIZED


@pytest.mark.django_db
def test_admin_user_can_post_agency(request_factory, admin_user):
    request: Response = request_factory.post('/api/v1/agencies/', {'name': 'Realtors, Inc.',
                                                                   'address': 'Someplace',
                                                                   'phone': '+12257678120'})

    view = views.AgencyViewSet.as_view({'post': 'create'})
    admin_user.refresh_from_db()
    force_authenticate(request, user=admin_user)
    response = view(request)

    assert response.status_code == status.HTTP_201_CREATED


@pytest.mark.django_db
def test_realtor_user_can_post_agency(request_factory, realtor_a: User):
    # note we can only assume mls is there because we know this is a realtor
    mls = MLSNumber.objects.get(user=realtor_a)
    request: Response = request_factory.patch('/api/v1/agencies/{}'.format(mls.agency.id),
                                              {'name': 'Realty, Inc.'})

    view = views.AgencyViewSet.as_view({'patch': 'partial_update'})
    realtor_a.refresh_from_db()
    force_authenticate(request, user=realtor_a)
    response = view(request)

    assert response.status_code == status.HTTP_201_CREATED

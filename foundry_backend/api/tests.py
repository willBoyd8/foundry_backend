import pytest
from django.contrib.auth.models import User
from requests import Response
from rest_framework import status
from rest_framework.authtoken.models import Token
from rest_framework.test import APIClient
from rest_framework.utils import json
from foundry_backend.api import views, access
from foundry_backend.database.models import Agency, MLSNumber


def perform_api_action(action, data, path, token):
    response = action(path, data=data, format='json', HTTP_AUTHORIZATION='Token {}'.format(token))
    return response


def perform_creation(token, client, data, path):
    return perform_api_action(client.post, data, path, token)


@pytest.mark.django_db
def test_agency_redirect(client):
    response = client.get('/api/v1/agencies')
    assert response.status_code == 301


def test_agency_permission():
    assert type(views.AgencyViewSet().access_policy()) == access.AgencyAccessPolicy


@pytest.mark.django_db
def test_anyone_can_get_agencies(client):
    response: Response = client.get('/api/v1/agencies/')
    assert response.status_code == 200
    assert response.json() == []


@pytest.mark.django_db
def test_unauthenticated_cannot_create_agency(client):
    data = {'name': 'Agency', 'phone': '+14035555319', 'address': 'Someplace Drive'}

    response: Response = client.post('/api/v1/agencies/', data)

    assert response.status_code == status.HTTP_401_UNAUTHORIZED


@pytest.mark.django_db
def test_admin_can_create_agency(admin_user):
    client = APIClient()

    data = {'name': 'Agency', 'phone': '+14035555319', 'address': 'Someplace Drive'}

    response = perform_api_action(client.post, data, '/api/v1/agencies/', admin_user[1])

    assert response.status_code == status.HTTP_201_CREATED
    assert json.loads(response.render().content) == {**data, 'id': 1}


def test_admin_can_put_agency(realtor_a, admin_user):
    client = APIClient()
    _, agency, _, _ = realtor_a

    data = {'name': 'Agency Alpha', 'phone': str(agency.phone), 'address': agency.address}

    response = perform_api_action(client.put, data, '/api/v1/agencies/{}/'.format(agency.id), admin_user[1])

    assert response.status_code == status.HTTP_200_OK

    assert json.loads(response.render().content) == {'name': 'Agency Alpha',
                                                     'address': agency.address,
                                                     'phone': agency.phone,
                                                     'id': agency.id}

    agency.refresh_from_db()

    assert agency.name == 'Agency Alpha'
    assert agency.id == agency.id
    assert agency.phone == agency.phone
    assert agency.address == agency.address


def test_admin_can_patch_agency(realtor_a, admin_user):
    client = APIClient()
    _, agency, _, _ = realtor_a
    _, token = admin_user

    path = '/api/v1/agencies/{}/'.format(agency.id)
    data = {'name': 'Different, Inc.'}
    action = client.patch

    response = perform_api_action(action, data, path, token)

    agency.refresh_from_db()

    assert response.status_code == status.HTTP_200_OK

    assert agency.name == 'Different, Inc.'
    assert agency.id == agency.id
    assert agency.phone == agency.phone
    assert agency.address == agency.address


def test_admin_can_delete_agency(realtor_a, admin_user):
    client = APIClient()
    _, agency, _, _ = realtor_a
    _, token = admin_user

    path = '/api/v1/agencies/{}/'.format(agency.id)
    action = client.delete

    response = perform_api_action(action, {}, path, token)

    assert response.status_code == status.HTTP_204_NO_CONTENT
    assert not Agency.objects.filter(id=agency.id).exists()


@pytest.mark.django_db
def test_realtor_cannot_create_agency(realtor_a):
    client = APIClient()

    data = {'name': 'Agency', 'phone': '+14035555319', 'address': 'Someplace Drive'}

    response = perform_api_action(client.post, data, '/api/v1/agencies/', realtor_a[3])

    assert realtor_a[1].mlsnumber_set.filter(user_id=realtor_a[0]).exists()

    assert response.status_code == status.HTTP_403_FORBIDDEN


def test_realtor_can_put_own_agency(realtor_a):
    client = APIClient()
    _, agency, _, token = realtor_a

    data = {'name': 'Agency Alpha', 'phone': str(agency.phone), 'address': agency.address}

    response = perform_api_action(client.put, data, '/api/v1/agencies/{}/'.format(agency.id), token)

    assert response.status_code == status.HTTP_200_OK

    assert json.loads(response.render().content) == {'name': 'Agency Alpha',
                                                     'address': agency.address,
                                                     'phone': agency.phone,
                                                     'id': agency.id}

    agency.refresh_from_db()

    assert agency.name == 'Agency Alpha'
    assert agency.id == agency.id
    assert agency.phone == agency.phone
    assert agency.address == agency.address


def test_realtor_can_patch_own_agency(realtor_a):
    client = APIClient()
    _, agency, _, token = realtor_a

    path = '/api/v1/agencies/{}/'.format(agency.id)
    data = {'name': 'Different, Inc.'}
    action = client.patch

    response = perform_api_action(action, data, path, token)

    agency.refresh_from_db()

    assert response.status_code == status.HTTP_200_OK

    assert agency.name == 'Different, Inc.'
    assert agency.id == agency.id
    assert agency.phone == agency.phone
    assert agency.address == agency.address


def test_realtor_cannot_delete_agency(realtor_a):
    client = APIClient()
    _, agency, _, token = realtor_a

    path = '/api/v1/agencies/{}/'.format(agency.id)
    action = client.delete

    response = perform_api_action(action, {}, path, token)

    assert response.status_code == status.HTTP_403_FORBIDDEN
    assert Agency.objects.filter(id=agency.id).exists()


def test_realtor_cannot_put_different_agency(realtor_a, realtor_b):
    client = APIClient()
    _, agency, _, _ = realtor_a
    _, _, _, token = realtor_b

    data = {'name': 'Agency Alpha', 'phone': str(agency.phone), 'address': agency.address}

    response = perform_api_action(client.put, data, '/api/v1/agencies/{}/'.format(agency.id), token)

    assert response.status_code == status.HTTP_403_FORBIDDEN

    agency.refresh_from_db()

    assert agency.name == agency.name
    assert agency.id == agency.id
    assert agency.phone == agency.phone
    assert agency.address == agency.address


def test_realtor_cannot_patch_different_agency(realtor_a, realtor_b):
    client = APIClient()
    _, agency, _, _ = realtor_a
    _, _, _, token = realtor_b

    path = '/api/v1/agencies/{}/'.format(agency.id)
    data = {'name': 'Different, Inc.'}
    action = client.patch

    response = perform_api_action(action, data, path, token)

    agency.refresh_from_db()

    assert response.status_code == status.HTTP_403_FORBIDDEN

    assert agency.name == agency.name
    assert agency.id == agency.id
    assert agency.phone == agency.phone
    assert agency.address == agency.address


def test_mls_number_permission():
    assert type(views.MLSNumberViewSet().access_policy()) == access.MLSNumberAccessPolicy


@pytest.mark.django_db
def test_anyone_can_get_mls_number(client, realtor_a):
    realtor, agency, mls, token = realtor_a

    response: Response = client.get('/api/v1/mls_numbers/')
    assert response.status_code == 200
    assert response.json() == [{'id': mls.id, 'agency': agency.id, 'number': str(mls.number), 'user': realtor.id}]


@pytest.mark.django_db
def test_anyone_cannot_create_mls_number(client):
    agency = Agency.objects.create(name='Alpha Agency', address='Someplace Drive', phone='+18626405799')
    realtor = User.objects.create_user(username='realtor_a', email='realtor_a@email.com', password='password')
    token = Token.objects.create(user=realtor)

    agency.save()
    realtor.save()
    token.save()

    response: Response = client.post('/api/v1/mls_numbers/', {'agency': agency.id, 'user': realtor.id})
    assert response.status_code == status.HTTP_401_UNAUTHORIZED


@pytest.mark.django_db
def test_admin_can_create_mls_number(client, admin_user):
    agency = Agency.objects.create(name='Alpha Agency', address='Someplace Drive', phone='+18626405799')
    realtor = User.objects.create_user(username='realtor_a', email='realtor_a@email.com', password='password')

    agency.save()
    realtor.save()

    data = {'agency': agency.id, 'user': realtor.id}
    response = perform_api_action(client.post, data, '/api/v1/mls_numbers/', admin_user[1])

    mls = MLSNumber.objects.filter(user_id=realtor.id).get()

    assert response.status_code == status.HTTP_201_CREATED
    assert response.json() == {'id': mls.id, 'agency': agency.id, 'number': str(mls.number), 'user': realtor.id}


@pytest.mark.django_db
def test_admin_can_put_mls_number(admin_user):
    client = APIClient()

    agency = Agency.objects.create(name='Alpha Agency', address='Someplace Drive', phone='+18626405799')
    realtor = User.objects.create_user(username='realtor_a', email='realtor_a@email.com', password='password')
    mls = MLSNumber.objects.create(agency=agency, user=realtor)

    agency.save()
    realtor.save()
    mls.save()

    new_agency = Agency.objects.create(name='Beta Agency', address='Someplace Road', phone='+18626405799')
    new_agency.save()

    data = {'agency': new_agency.id, 'user': realtor.id}
    response = perform_api_action(client.put, data, '/api/v1/mls_numbers/{}/'.format(mls.id), admin_user[1])

    assert response.status_code == status.HTTP_200_OK
    assert response.json() == {'id': mls.id, 'agency': new_agency.id, 'user': realtor.id, 'number': str(mls.number)}


@pytest.mark.django_db
def test_admin_can_patch_mls_number(admin_user):
    client = APIClient()

    agency = Agency.objects.create(name='Alpha Agency', address='Someplace Drive', phone='+18626405799')
    realtor = User.objects.create_user(username='realtor_a', email='realtor_a@email.com', password='password')
    mls = MLSNumber.objects.create(agency=agency, user=realtor)

    agency.save()
    realtor.save()
    mls.save()

    new_agency = Agency.objects.create(name='Beta Agency', address='Someplace Road', phone='+18626405799')
    new_agency.save()

    data = {'agency': new_agency.id}
    response = perform_api_action(client.patch, data, '/api/v1/mls_numbers/{}/'.format(mls.id), admin_user[1])

    assert response.status_code == status.HTTP_200_OK
    assert response.json() == {'id': mls.id, 'agency': new_agency.id, 'user': realtor.id, 'number': str(mls.number)}


@pytest.mark.django_db
def test_admin_can_delete_mls_number(admin_user):
    client = APIClient()

    agency = Agency.objects.create(name='Alpha Agency', address='Someplace Drive', phone='+18626405799')
    realtor = User.objects.create_user(username='realtor_a', email='realtor_a@email.com', password='password')
    mls = MLSNumber.objects.create(agency=agency, user=realtor)

    agency.save()
    realtor.save()
    mls.save()

    response = perform_api_action(client.delete, {}, '/api/v1/mls_numbers/{}/'.format(mls.id), admin_user[1])

    assert response.status_code == status.HTTP_204_NO_CONTENT
    assert not MLSNumber.objects.filter(id=mls.id).exists()


def test_nearby_attraction_permission():
    assert type(views.NearbyAttractionViewSet().access_policy()) == access.RealtorAdminAccessPolicy


@pytest.mark.django_db
def test_anyone_can_get_nearby_attractions(client):
    response: Response = client.get('/api/v1/nearby_attractions/')
    assert response.status_code == 200
    assert response.json() == []


@pytest.mark.django_db
def test_unauthenticated_cannot_create_nearby_attraction(client):
    data = {'name': 'Movie Theater', 'type': 'ENTERTAINMENT'}

    response: Response = client.post('/api/v1/nearby_attractions/', data)

    assert response.status_code == status.HTTP_401_UNAUTHORIZED


@pytest.mark.django_db
def test_admin_can_create_nearby_attractions(admin_user):
    client = APIClient()

    data = {'name': 'Movie Theater', 'type': 'ENTERTAINMENT'}

    response = perform_creation(admin_user[1],
                                client,
                                data,
                                '/api/v1/nearby_attractions/')

    assert response.status_code == status.HTTP_201_CREATED
    assert json.loads(response.render().content) == {**data, 'id': 1}


@pytest.mark.django_db
def test_realtor_can_create_nearby_attractions(realtor_a):
    client = APIClient()

    data = {'name': 'Movie Theater', 'type': 'ENTERTAINMENT'}

    response = perform_creation(realtor_a[3],
                                client,
                                data,
                                '/api/v1/nearby_attractions/')

    assert response.status_code == status.HTTP_201_CREATED
    assert json.loads(response.render().content) == {**data, 'id': 1}


def test_property_permission():
    assert type(views.PropertyViewSet().access_policy()) == access.InterAgencyListingAccessPolicy


def test_nearby_attraction_property_connector_permission():
    assert type(views.NearbyAttractionPropertyConnectorViewSet().access_policy()) == access.RealtorAdminAccessPolicy


def test_realtor_can_change_owned_listing(realtor_c, listing_a):
    client = APIClient()

    data = {'agent': realtor_c[2].id}
    response = perform_api_action(client.patch, data, '/api/v1/listings/{}/'.format(listing_a.id), realtor_c[3])

    listing_a.refresh_from_db()

    assert response.status_code == status.HTTP_200_OK
    assert response.json() == {'id': listing_a.id, 'agent': listing_a.agent.id,
                               'asking_price': listing_a.asking_price, 'description': listing_a.description}


def test_realtor_cannot_change_non_owned_listing(realtor_b, listing_a):
    client = APIClient()

    data = {'agent': realtor_b[2].id}
    response = perform_api_action(client.patch, data, '/api/v1/listings/{}/'.format(listing_a.id), realtor_b[3])

    listing_a.refresh_from_db()

    assert response.status_code == status.HTTP_403_FORBIDDEN


def test_realtor_can_change_owned_property(realtor_c, listing_a):
    client = APIClient()

    data = {'square_footage': 3000}
    response = perform_api_action(client.patch, data, '/api/v1/properties/{}/'.format(listing_a.property.id), realtor_c[3])

    listing_a.refresh_from_db()

    assert response.status_code == status.HTTP_200_OK
    assert response.json() == {'id': listing_a.property.id, 'square_footage': 3000,
                               'address': listing_a.property.address.to_dict(), 'listing': listing_a.id,
                               'type': listing_a.property.type}


def test_realtor_cannot_change_non_owned_property(realtor_b, listing_a):
    client = APIClient()

    data = {'square_footage': 3000}
    response = perform_api_action(client.patch, data, '/api/v1/properties/{}/'.format(listing_a.property.id), realtor_b[3])

    listing_a.refresh_from_db()

    assert response.status_code == status.HTTP_403_FORBIDDEN

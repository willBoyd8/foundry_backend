import datetime
from typing import List, Tuple
from unittest.mock import MagicMock, patch, call
from uuid import UUID

import pytest
from django.contrib.auth.models import User
from requests import Response
from rest_framework import status
from rest_framework.authtoken.models import Token
from rest_framework.test import APIClient
from rest_framework.utils import json
from foundry_backend.api import views, serializers
from foundry_backend.api.models import IAMPolicy
from foundry_backend.database.apps import DatabaseConfig
from foundry_backend.database.models import Agency, MLSNumber, Listing, Address, UserMessage, NearbyAttraction, \
    listing_path_generator, avatar_path_generator


def check_list_equal(first: List, second: List):
    return len(first) == len(second) and sorted(first) == sorted(second)


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
    assert type(views.AgencyViewSet().access_policy()).__name__ == 'AgencyAccessPolicy'


def test_user_message_permission():
    assert type(views.UserMessageViewSet().access_policy()).__name__ == 'UserMessageAccessPolicy'


def test_avatar_permission():
    assert type(views.AvatarViewSet().access_policy()).__name__ == 'AvatarAccessPolicy'


def test_mls_number_permission():
    assert type(views.MLSNumberViewSet().access_policy()).__name__ == 'MLSNumberAccessPolicy'


def test_all_mls_number_permission():
    assert type(views.AllMLSNumbersViewSet().access_policy()).__name__ == 'MLSNumberAccessPolicy'


def test_nearby_attraction_permission():
    assert type(views.NearbyAttractionViewSet().access_policy()).__name__ == 'RealtorAdminAccessPolicy'


def test_property_permission():
    assert type(views.PropertyViewSet().access_policy()).__name__ == 'InterAgencyListingAccessPolicy'


def test_nearby_attraction_property_connector_permission():
    assert type(views.NearbyAttractionPropertyConnectorViewSet().access_policy()).__name__ == 'RealtorAdminAccessPolicy'


def test_listing_permission():
    assert type(views.ListingViewSet().access_policy()).__name__ == 'InterAgencyListingAccessPolicy'


def test_listings_hit_permission():
    assert type(views.ListingsHitViewSet().access_policy()).__name__ == 'ListingsHitAccessPolicy'


def test_listing_image_permission():
    assert type(views.ListingImageViewSet().access_policy()).__name__ == 'InterAgencyListingAccessPolicy'


def test_iam_policy_permission():
    assert type(views.IAMPolicyViewSet().access_policy()).__name__ == 'IAMPolicyAccessPolicy'


def test_iam_policy_statement_permission():
    assert type(views.IAMPolicyStatementViewSet().access_policy()).__name__ == 'IAMPolicyAccessPolicy'
    

def test_iam_policy_statement_principal_permission():
    assert type(views.IAMPolicyStatementPrincipalViewSet().access_policy()).__name__ == 'IAMPolicyAccessPolicy'


def test_iam_policy_statement_condition_permission():
    assert type(views.IAMPolicyStatementConditionViewSet().access_policy()).__name__ == 'IAMPolicyAccessPolicy'


def test_showing_permission():
    assert type(views.ShowingViewSet().access_policy()).__name__ == 'ShowingAccessPolicy'


def test_showing_review_permission():
    assert type(views.ShowingReviewViewSet().access_policy()).__name__ == 'ShowingReviewAccessPolicy'


# def test_all_nearby_attractions_permission():
#     assert type(views.AllNearbyAttractionsViewSet().access_policy()).__name__ == 'RealtorAdminAccessPolicy'


def test_home_alarm_permission():
    assert type(views.HomeAlarmViewSet().access_policy()).__name__ == 'HomeAlarmAccessPolicy'


@pytest.mark.django_db
def test_anyone_can_get_agencies(client, setup):
    response: Response = client.get('/api/v1/agencies/')
    assert response.status_code == 200
    assert response.json() == []


@pytest.mark.django_db
def test_unauthenticated_cannot_create_agency(client, setup):
    data = {'name': 'Agency', 'phone': '+14035555319', 'address': 'Someplace Drive'}

    response: Response = client.post('/api/v1/agencies/', data)

    assert response.status_code == status.HTTP_401_UNAUTHORIZED


def test_admin_can_create_agency(admin_user, setup):
    client = APIClient()

    data = {
        'name': 'Agency',
        'phone': '+14035555319',
        'mls_numbers': [],
        'address': dict(street_number='1516',
                        street='Big Cove Road',
                        postal_code='35801',
                        locality='Huntsville',
                        state_code='AL',
                        state='Alabama')
    }

    response = perform_api_action(client.post, data, '/api/v1/agencies/', admin_user[1])

    assert response.status_code == status.HTTP_201_CREATED
    assert json.loads(response.render().content) == {**data, 'id': 1}


def test_admin_can_patch_agency(realtor_a, admin_user, setup):
    client = APIClient()
    _, agency, _, _ = realtor_a

    data = {
        'name': 'Agency Alpha',
        'phone': str(agency.phone),
        'mls_numbers': []
    }

    response = perform_api_action(client.patch, data, '/api/v1/agencies/{}/'.format(agency.id), admin_user[1])

    assert response.status_code == status.HTTP_200_OK

    assert json.loads(response.render().content) == {'name': 'Agency Alpha',
                                                     'mls_numbers': [],
                                                     'address': agency.address.to_dict(),
                                                     'phone': str(agency.phone),
                                                     'id': agency.id}

    agency.refresh_from_db()

    assert agency.name == 'Agency Alpha'
    assert agency.id == agency.id
    assert agency.phone == str(agency.phone)
    assert agency.address == agency.address


# def test_admin_can_patch_agency(realtor_a, admin_user):
#     client = APIClient()
#     _, agency, _, _ = realtor_a
#     _, token = admin_user
#
#     path = '/api/v1/agencies/{}/'.format(agency.id)
#     data = {'name': 'Different, Inc.'}
#     action = client.patch
#
#     response = perform_api_action(action, data, path, token)
#
#     agency.refresh_from_db()
#
#     assert response.status_code == status.HTTP_200_OK
#
#     assert agency.name == 'Different, Inc.'
#     assert agency.id == agency.id
#     assert agency.phone == agency.phone
#     assert agency.address == agency.address


def test_admin_can_delete_agency(realtor_a, admin_user, setup):
    client = APIClient()
    _, agency, _, _ = realtor_a
    _, token = admin_user

    path = '/api/v1/agencies/{}/'.format(agency.id)
    action = client.delete

    response = perform_api_action(action, {}, path, token)

    assert response.status_code == status.HTTP_204_NO_CONTENT
    assert not Agency.objects.filter(id=agency.id).exists()


@pytest.mark.django_db
def test_realtor_cannot_create_agency(realtor_a, setup):
    client = APIClient()

    data = {'name': 'Agency', 'phone': '+14035555319', 'address': 'Someplace Drive'}

    response = perform_api_action(client.post, data, '/api/v1/agencies/', realtor_a[3])

    assert realtor_a[1].mls_numbers.filter(user_id=realtor_a[0]).exists()

    assert response.status_code == status.HTTP_403_FORBIDDEN


def test_realtor_can_patch_own_agency(realtor_a, setup):
    client = APIClient()
    _, agency, _, token = realtor_a

    data = {'name': 'Agency Alpha', 'phone': str(agency.phone), 'mls_numbers': []}

    response = perform_api_action(client.patch, data, '/api/v1/agencies/{}/'.format(agency.id), token)

    assert response.status_code == status.HTTP_200_OK

    assert json.loads(response.render().content) == {'name': 'Agency Alpha',
                                                     'address': agency.address.to_dict(),
                                                     'phone': str(agency.phone),
                                                     'mls_numbers': [],
                                                     'id': agency.id}

    agency.refresh_from_db()

    assert agency.name == 'Agency Alpha'
    assert agency.id == agency.id
    assert agency.phone == agency.phone
    assert agency.address == agency.address


def test_realtor_cannot_delete_agency(realtor_a, setup):
    client = APIClient()
    _, agency, _, token = realtor_a

    path = '/api/v1/agencies/{}/'.format(agency.id)
    action = client.delete

    response = perform_api_action(action, {}, path, token)

    assert response.status_code == status.HTTP_403_FORBIDDEN
    assert Agency.objects.filter(id=agency.id).exists()


def test_realtor_cannot_patch_different_agency(realtor_a, realtor_b, setup):
    client = APIClient()
    _, agency, _, _ = realtor_a
    _, _, _, token = realtor_b

    data = {'name': 'Agency Alpha', 'phone': str(agency.phone)}

    response = perform_api_action(client.patch, data, '/api/v1/agencies/{}/'.format(agency.id), token)

    assert response.status_code == status.HTTP_403_FORBIDDEN

    agency.refresh_from_db()

    assert agency.name == agency.name
    assert agency.id == agency.id
    assert agency.phone == agency.phone
    assert agency.address == agency.address


@pytest.mark.django_db
def test_anyone_can_get_mls_number(client, realtor_a, setup):
    realtor, agency, mls, token = realtor_a

    response: Response = client.get('/api/v1/agencies/{}/mls_numbers/'.format(agency.id))
    assert response.status_code == 200
    assert response.json() == [
        {
            'id': mls.id,
            'number': str(mls.number),
            'user': realtor.id,
            'user_info': {
                'email': realtor.email,
                'first_name': realtor.first_name,
                'last_name': realtor.last_name,
                'username': realtor.username
            }
        }
    ]


@pytest.mark.django_db
def test_anyone_cannot_create_mls_number(client, setup):
    address = Address(street_number='1518', street='Big Cove Road', postal_code='35801', locality='Huntsville',
                      state_code='AL', state='Alabama')
    address.save()
    agency = Agency.objects.create(name='Alpha Agency', address=address, phone='+18626405799')
    realtor = User.objects.create_user(username='realtor_a', email='realtor_a@email.com', password='password')
    token = Token.objects.create(user=realtor)

    agency.save()
    realtor.save()
    token.save()

    response: Response = client.post('/api/v1/agencies/{}/mls_numbers/'.format(agency.id), {'user': realtor.id})
    assert response.status_code == status.HTTP_401_UNAUTHORIZED


@pytest.mark.django_db
def test_admin_can_create_mls_number(client, admin_user, setup):
    address = Address(street_number='1518', street='Big Cove Road', postal_code='35801', locality='Huntsville',
                      state_code='AL', state='Alabama')
    address.save()
    agency = Agency.objects.create(name='Alpha Agency', address=address, phone='+18626405799')
    realtor = User.objects.create_user(username='realtor_a', email='realtor_a@email.com', password='password',
                                       first_name='Alpha', last_name='Realtor')

    agency.save()
    realtor.save()

    data = {'user': realtor.id}
    response = perform_api_action(client.post, data, '/api/v1/agencies/{}/mls_numbers/'.format(agency.id),
                                  admin_user[1])

    assert response.status_code == status.HTTP_201_CREATED

    mls = MLSNumber.objects.filter(user=realtor).get()

    assert response.json() == {'user': realtor.id,
                               'user_info': {'email': realtor.email,
                                             'first_name': realtor.first_name,
                                             'last_name': realtor.last_name,
                                             'username': realtor.username
                                             }
                               }


@pytest.mark.django_db
def test_admin_cannot_create_duplicate_mls_number(client, admin_user, realtor_a, setup):
    realtor, _, mls_number, _ = realtor_a

    data = {'user': realtor.id}
    response = perform_api_action(client.post, data, '/api/v1/agencies/{}/mls_numbers/'.format(mls_number.agency.id),
                                  admin_user[1])

    assert response.status_code == status.HTTP_400_BAD_REQUEST


@pytest.mark.django_db
def test_admin_can_put_mls_number(admin_user, setup):
    client = APIClient()

    address = Address(street_number='1518', street='Big Cove Road', postal_code='35801', locality='Huntsville',
                      state_code='AL', state='Alabama')
    address.save()

    agency = Agency.objects.create(name='Alpha Agency', address=address, phone='+18626405799')
    realtor = User.objects.create_user(username='realtor_a', email='realtor_a@email.com', password='password')
    mls = MLSNumber.objects.create(agency=agency, user=realtor)

    agency.save()
    realtor.save()
    mls.save()

    address_beta = Address(street_number='1519', street='Big Cove Road', postal_code='35801', locality='Huntsville',
                           state_code='AL', state='Alabama')
    address_beta.save()

    new_agency = Agency.objects.create(name='Beta Agency', address=address_beta, phone='+18626405799')
    new_agency.save()

    data = {'agency': new_agency.id, 'user': realtor.id}
    response = perform_api_action(client.put, data, '/api/v1/agencies/{}/mls_numbers/{}/'.format(agency.id, mls.id),
                                  admin_user[1])

    assert response.status_code == status.HTTP_200_OK
    assert response.json() == {
        'id': mls.id,
        'user': realtor.id,
        'number': str(mls.number),
        'user_info': {
            'email': realtor.email,
            'first_name': realtor.first_name,
            'last_name': realtor.last_name,
            'username': realtor.username
        }
    }


@pytest.mark.django_db
def test_admin_can_patch_mls_number(admin_user, setup):
    client = APIClient()

    address = Address(street_number='1518', street='Big Cove Road', postal_code='35801', locality='Huntsville',
                      state_code='AL', state='Alabama')
    address.save()

    agency = Agency.objects.create(name='Alpha Agency', address=address, phone='+18626405799')
    realtor = User.objects.create_user(username='realtor_a', email='realtor_a@email.com', password='password')
    mls = MLSNumber.objects.create(agency=agency, user=realtor)

    agency.save()
    realtor.save()
    mls.save()

    address_beta = Address(street_number='1519', street='Big Cove Road', postal_code='35801', locality='Huntsville',
                           state_code='AL', state='Alabama')
    address_beta.save()

    new_agency = Agency.objects.create(name='Beta Agency', address=address_beta, phone='+18626405799')
    new_agency.save()

    data = {'agency': new_agency.id}
    response = perform_api_action(client.patch, data, '/api/v1/agencies/{}/mls_numbers/{}/'.format(agency.id, mls.id),
                                  admin_user[1])

    assert response.status_code == status.HTTP_200_OK
    assert response.json() == {
        'id': mls.id,
        'user': realtor.id,
        'number': str(mls.number),
        'user_info': {
            'email': realtor.email,
            'first_name': realtor.first_name,
            'last_name': realtor.last_name,
            'username': realtor.username
        }
    }


@pytest.mark.django_db
def test_admin_can_delete_mls_number(admin_user, setup):
    client = APIClient()

    address = Address(street_number='1518', street='Big Cove Road', postal_code='35801', locality='Huntsville',
                      state_code='AL', state='Alabama')
    address.save()

    agency = Agency.objects.create(name='Alpha Agency', address=address, phone='+18626405799')
    realtor = User.objects.create_user(username='realtor_a', email='realtor_a@email.com', password='password')
    mls = MLSNumber.objects.create(agency=agency, user=realtor)

    agency.save()
    realtor.save()
    mls.save()

    response = perform_api_action(client.delete, {}, '/api/v1/agencies/{}/mls_numbers/{}/'.format(agency.id, mls.id),
                                  admin_user[1])

    assert response.status_code == status.HTTP_204_NO_CONTENT
    assert not MLSNumber.objects.filter(id=mls.id).exists()


# @pytest.mark.django_db
# def test_anyone_can_get_nearby_attractions(client):
#     response: Response = client.get('/api/v1/nearby_attractions/')
#     assert response.status_code == 200
#     assert response.json() == []


def test_anyone_can_get_listing_nearby_attractions(client, listing_a: Listing, setup):
    response: Response = client.get(
        '/api/v1/listings/{}/property/{}/nearby_attractions/'.format(listing_a.id, listing_a.property.id)
    )

    assert response.status_code == status.HTTP_200_OK

    nearby_attraction_ids = [attraction.id for attraction in listing_a.property.nearby_attractions.all()]
    response_ids = [attraction.get('id') for attraction in response.json()]

    assert response_ids == nearby_attraction_ids

@pytest.mark.django_db
def test_unauthenticated_cannot_create_nearby_attraction(client, listing_a, setup):
    data = {'name': 'Movie Theater', 'type': 'ENTERTAINMENT'}

    response: Response = client.post(
        '/api/v1/listings/{}/property/{}/nearby_attractions/'.format(listing_a.id, listing_a.property.id),
        data
    )

    assert response.status_code == status.HTTP_401_UNAUTHORIZED


@pytest.mark.django_db
def test_admin_can_create_nearby_attractions(admin_user, listing_a, setup):
    client = APIClient()

    data = {'name': 'Movie Theater', 'type': 'ENTERTAINMENT'}

    response = perform_creation(
        admin_user[1],
        client,
        data,
        '/api/v1/listings/{}/property/{}/nearby_attractions/'.format(
            listing_a.id,
            listing_a.property.id
        )
    )

    assert response.status_code == status.HTTP_201_CREATED
    assert json.loads(response.render().content) == {**data}


@pytest.mark.django_db
def test_realtor_can_create_nearby_attractions(realtor_a, listing_a, setup):
    client = APIClient()

    data = {'name': 'Movie Theater', 'type': 'ENTERTAINMENT'}

    response = perform_creation(
        realtor_a[3],
        client,
        data,
        '/api/v1/listings/{}/property/{}/nearby_attractions/'.format(
            listing_a.id,
            listing_a.property.id
        )
    )

    assert response.status_code == status.HTTP_201_CREATED
    assert json.loads(response.render().content) == {**data}


def test_listing_duplicate_rooms_caught(realtor_a, setup):
    client = APIClient()

    data = {
        'agent': realtor_a[0].id,
        'asking_price': 500000,
        'description': 'Custom built home with lots of light and a beautiful treed '
                       'lot. Hardwoods in the formals plus a study & library that '
                       'open to a rear flagstone patio. Formerly owned by Dr. Wernher '
                       'von Braun.',
        'property': {
            'address': {
                'street_number': '1516',
                'street': 'Big Cove Road',
                'locality': 'Huntsville',
                'postal_code': '35801',
                'state': 'Alabama',
                'state_code': 'AL'
            },
            'square_footage': 2750,
            'acreage': 1.25,
            'type': 'HOUSE',
            'rooms': [
                {
                    'name': 'Master Bedroom',
                    'description': 'Nice room with view of backyard',
                    'type': 'BEDROOM',
                    'square_footage': 100
                },
                {
                    'name': 'Master Bedroom',
                    'type': 'BEDROOM',
                    'square_footage': 26
                }
            ],
            'nearby_attractions': [],
            'home_alarm': {
                'arm_code': '1234',
                'disarm_code': '2345',
                'password': 'password',
                'notes': 'Don\'t push the red button...'
            }
        }
    }

    response = perform_api_action(client.post, data, '/api/v1/listings/', realtor_a[3])

    assert response.status_code == status.HTTP_400_BAD_REQUEST

    assert response.json() == {'property': {'rooms': ['Room names must be unique']}}


def test_listing_duplicate_attractions_caught(realtor_a, setup):
    client = APIClient()

    data = {
        'agent': realtor_a[0].id,
        'asking_price': 500000,
        'description': 'Custom built home with lots of light and a beautiful treed '
                       'lot. Hardwoods in the formals plus a study & library that '
                       'open to a rear flagstone patio. Formerly owned by Dr. Wernher '
                       'von Braun.',
        'property': {
            'address': {
                'street_number': '1516',
                'street': 'Big Cove Road',
                'locality': 'Huntsville',
                'postal_code': '35801',
                'state': 'Alabama',
                'state_code': 'AL'
            },
            'square_footage': 2750,
            'acreage': 1.25,
            'type': 'HOUSE',
            'rooms': [
                {
                    'name': 'Master Bedroom',
                    'description': 'Nice room with view of backyard',
                    'type': 'BEDROOM',
                    'square_footage': 123
                }
            ],
            'nearby_attractions': [
                {
                    'name': 'Some School',
                    'type': 'SCHOOL_PRIVATE'
                },
                {
                    'name': 'Some School',
                    'type': 'SCHOOL_ELEM'
                }
            ],
            'home_alarm': {
                'arm_code': '1234',
                'disarm_code': '2345',
                'password': 'password',
                'notes': 'Don\'t push the red button...'
            }
        }
    }

    response = perform_api_action(client.post, data, '/api/v1/listings/', realtor_a[3])

    assert response.status_code == status.HTTP_400_BAD_REQUEST

    assert response.json() == {'property': {'nearby_attractions': ['Nearby Attraction names must be unique']}}


def test_anyone_can_get_listing(client, listing_a, listing_b, listing_c, listing_d, listing_e, setup):
    response: Response = client.get('/api/v1/listings/')

    listing_ids = [r.get('id') for r in response.json()]

    assert response.status_code == status.HTTP_200_OK
    assert listing_a.id in listing_ids
    assert listing_b.id in listing_ids
    assert listing_c.id in listing_ids
    assert listing_d.id in listing_ids
    assert listing_e.id in listing_ids


def test_filter_listing_by_open_state(client, listing_a, listing_b, listing_c, listing_d, listing_e, setup):
    response: Response = client.get('/api/v1/listings/', {'open': True})

    listing_ids = [r.get('id') for r in response.json()]

    assert response.status_code == status.HTTP_200_OK
    assert listing_a.id in listing_ids
    assert listing_b.id in listing_ids
    assert listing_c.id in listing_ids
    assert listing_d.id in listing_ids
    assert listing_e.id not in listing_ids


def test_filter_listing_by_closed_state(client, listing_a, listing_b, listing_c, listing_d, listing_e, setup):
    response: Response = client.get('/api/v1/listings/', {'open': False})

    listing_ids = [r.get('id') for r in response.json()]

    assert response.status_code == status.HTTP_200_OK
    assert listing_a.id not in listing_ids
    assert listing_b.id not in listing_ids
    assert listing_c.id not in listing_ids
    assert listing_d.id not in listing_ids
    assert listing_e.id in listing_ids


def test_realtor_can_create_listing(realtor_a, setup):
    client = APIClient()

    data = {
        'agent': realtor_a[0].id,
        'asking_price': 500000,
        'description': 'Custom built home with lots of light and a beautiful treed '
                       'lot. Hardwoods in the formals plus a study & library that '
                       'open to a rear flagstone patio. Formerly owned by Dr. Wernher '
                       'von Braun.',
        'property': {
            'address': {
                'street_number': '1516',
                'street': 'Big Cove Road',
                'locality': 'Huntsville',
                'postal_code': '35801',
                'state': 'Alabama',
                'state_code': 'AL'
            },
            'square_footage': 2750,
            'acreage': 1.25,
            'type': 'HOUSE',
            'rooms': [],
            'nearby_attractions': [],
            'home_alarm': {
                'arm_code': '1234',
                'disarm_code': '2345',
                'password': 'password',
                'notes': 'Don\'t push the red button...'
            }
        }
    }

    response = perform_api_action(client.post, data, '/api/v1/listings/', realtor_a[3])

    assert response.status_code == status.HTTP_201_CREATED

    listing = Listing.objects.get(property__address__street='Big Cove Road')

    listing_data = response.json()

    assert listing is not None
    assert listing.id == listing_data['id']


def test_realtor_can_change_owned_listing(realtor_c, listing_a, setup):
    client = APIClient()

    data = {'agent': realtor_c[0].id}

    response = perform_api_action(client.patch, data, '/api/v1/listings/{}/'.format(listing_a.id), realtor_c[3])

    listing_a.refresh_from_db()
    listing_data = serializers.ListingSerializer(listing_a).data

    assert response.status_code == status.HTTP_200_OK
    assert response.json() == listing_data


def test_realtor_cannot_change_non_owned_listing(realtor_b, listing_a, setup):
    client = APIClient()

    data = {'agent': realtor_b[2].id}
    response = perform_api_action(client.put, data, '/api/v1/listings/{}/'.format(listing_a.id), realtor_b[3])

    listing_a.refresh_from_db()

    assert response.status_code == status.HTTP_403_FORBIDDEN


def test_realtor_cannot_change_non_owned_property(realtor_b, listing_a, setup):
    client = APIClient()

    data = {'square_footage': 3000}
    response = perform_api_action(client.patch, data,
                                  '/api/v1/listings/{}/property/{}/'.format(listing_a.id, listing_a.property.id),
                                  realtor_b[3])

    listing_a.refresh_from_db()

    assert response.status_code == status.HTTP_403_FORBIDDEN


def test_anyone_can_access_policies(policy, client, setup):
    policy_obj: IAMPolicy = policy[0]

    response: Response = client.get('/api/v1/iam_policies/{}/'.format(policy_obj.id))

    assert response.status_code == 200

    # Check the policy
    response_data = response.json()
    assert response_data.get('id') == policy_obj.id
    assert response_data.get('name') == policy_obj.name

    # Check the first policy statement
    assert len(response_data.get('statements')) == len(policy_obj.statements.all())
    assert len(response_data.get('statements')) == 1
    assert len(policy_obj.statements.all()) == 1

    first_statement_data = response_data.get('statements')[0]
    first_statement_obj = policy_obj.statements.first()
    assert check_list_equal(first_statement_data.get('actions'), first_statement_obj.actions)

    # check the statement scalars
    assert first_statement_data.get('effect') == first_statement_obj.effect
    assert first_statement_data.get('notes') == first_statement_obj.notes

    # Check the conditions
    assert len(first_statement_data.get('conditions')) == len(first_statement_obj.conditions.all())
    assert len(first_statement_data.get('conditions')) == 1
    assert len(first_statement_obj.conditions.all()) == 1

    first_condition_data = first_statement_data.get('conditions')[0]
    first_condition_obj = first_statement_obj.conditions.first()
    assert first_condition_data.get('value') == first_condition_obj.value

    # Check the conditions
    assert len(first_statement_data.get('principals')) == len(first_statement_obj.principals.all())
    assert len(first_statement_data.get('principals')) == 1
    assert len(first_statement_obj.principals.all()) == 1

    first_condition_data = first_statement_data.get('principals')[0]
    first_condition_obj = first_statement_obj.principals.first()
    assert first_condition_data.get('value') == first_condition_obj.value


def test_anyone_cannot_create_access_policies(policy, client, setup):
    policy_obj: IAMPolicy = policy[0]
    policy_data: dict = policy[1]
    policy_obj.delete()

    response: Response = client.post('/api/v1/iam_policies/', policy_data)

    assert response.status_code == status.HTTP_401_UNAUTHORIZED


def test_admin_can_create_access_policies(policy, admin_user, setup):
    client = APIClient()

    policy_obj: IAMPolicy = policy[0]
    policy_data: dict = policy[1]
    policy_obj.delete()

    response: Response = perform_api_action(client.post, policy_data, '/api/v1/iam_policies/', admin_user[1])

    assert response.status_code == status.HTTP_201_CREATED


def test_filtering_agency_by_state_with_response(client, realtor_a, realtor_b, setup):
    _, agency_a, _, _ = realtor_a
    _, agency_b, _, _ = realtor_b

    response = client.get('/api/v1/agencies/', {'state': 'AL'})

    response_data = response.json()

    assert response.status_code == 200
    assert len(response_data) == 1

    response_ids = [r.get('id') for r in response_data]

    assert agency_a.id in response_ids
    assert agency_b.id not in response_ids


def test_filtering_agency_by_state_with_empty_response(client, realtor_a, realtor_b, setup):
    _, agency_a, _, _ = realtor_a
    _, agency_b, _, _ = realtor_b

    response = client.get('/api/v1/agencies/', {'state': 'tn'})

    response_data = response.json()

    assert response.status_code == 200
    assert len(response_data) == 0

    response_ids = [r.get('id') for r in response_data]

    assert agency_a.id not in response_ids
    assert agency_b.id not in response_ids


def test_filtering_agency_by_city_with_response(client, realtor_a, realtor_b, setup):
    _, agency_a, _, _ = realtor_a
    _, agency_b, _, _ = realtor_b

    response = client.get('/api/v1/agencies/', {'city': 'huntsville'})

    response_data = response.json()

    assert response.status_code == 200
    assert len(response_data) == 1

    response_ids = [r.get('id') for r in response_data]

    assert agency_a.id in response_ids
    assert agency_b.id not in response_ids


def test_filtering_agency_by_city_with_empty_response(client, realtor_a, realtor_b, setup):
    _, agency_a, _, _ = realtor_a
    _, agency_b, _, _ = realtor_b

    response = client.get('/api/v1/agencies/', {'city': 'pintlala'})

    response_data = response.json()

    assert response.status_code == 200
    assert len(response_data) == 0

    response_ids = [r.get('id') for r in response_data]

    assert agency_a.id not in response_ids
    assert agency_b.id not in response_ids


def test_filtering_agency_by_city_and_state_with_response(client, realtor_a, realtor_b, setup):
    _, agency_a, _, _ = realtor_a
    _, agency_b, _, _ = realtor_b

    response = client.get('/api/v1/agencies/', {'city': 'huntsville', 'state': 'al'})

    response_data = response.json()

    assert response.status_code == 200
    assert len(response_data) == 1

    response_ids = [r.get('id') for r in response_data]

    assert agency_a.id in response_ids
    assert agency_b.id not in response_ids


def test_filtering_agency_by_city_and_state_with_empty_response(client, realtor_a, realtor_b, setup):
    _, agency_a, _, _ = realtor_a
    _, agency_b, _, _ = realtor_b

    response = client.get('/api/v1/agencies/', {'city': 'madison', 'state': 'al'})

    response_data = response.json()

    assert response.status_code == 200
    assert len(response_data) == 0

    response_ids = [r.get('id') for r in response_data]

    assert agency_a.id not in response_ids
    assert agency_b.id not in response_ids


def test_filtering_property_by_min_asking_price(client, listing_a, listing_b, listing_c, listing_d, setup):
    response = client.get('/api/v1/listings/', {'asking_price_min': 600500})

    response_data = response.json()

    assert response.status_code == 200
    assert len(response_data) == 2

    response_ids = [r.get('id') for r in response_data]

    assert listing_a.id not in response_ids
    assert listing_b.id not in response_ids
    assert listing_c.id in response_ids
    assert listing_d.id in response_ids


def test_filtering_property_by_max_asking_price(client, listing_a, listing_b, listing_c, listing_d, setup):
    response = client.get('/api/v1/listings/', {'asking_price_max': 600500})

    response_data = response.json()

    assert response.status_code == 200
    assert len(response_data) == 2

    response_ids = [r.get('id') for r in response_data]

    assert listing_a.id in response_ids
    assert listing_b.id in response_ids
    assert listing_c.id not in response_ids
    assert listing_d.id not in response_ids


def test_filtering_property_by_min_and_max_asking_price(client, listing_a, listing_b, listing_c, listing_d, setup):
    response = client.get('/api/v1/listings/', {'asking_price_min': 500500, 'asking_price_max': 700500})

    response_data = response.json()

    assert response.status_code == 200
    assert len(response_data) == 2

    response_ids = [r.get('id') for r in response_data]

    assert listing_a.id not in response_ids
    assert listing_b.id in response_ids
    assert listing_c.id in response_ids
    assert listing_d.id not in response_ids


def test_filtering_property_by_min_square_footage(client, listing_a, listing_b, listing_c, listing_d, setup):
    response = client.get('/api/v1/listings/', {'square_footage_min': 3050})

    response_data = response.json()

    assert response.status_code == 200
    assert len(response_data) == 2

    response_ids = [r.get('id') for r in response_data]

    assert listing_a.id not in response_ids
    assert listing_b.id not in response_ids
    assert listing_c.id in response_ids
    assert listing_d.id in response_ids


def test_filtering_property_by_max_square_footage(client, listing_a, listing_b, listing_c, listing_d, setup):
    response = client.get('/api/v1/listings/', {'square_footage_max': 3050})

    response_data = response.json()

    assert response.status_code == 200
    assert len(response_data) == 2

    response_ids = [r.get('id') for r in response_data]

    assert listing_a.id in response_ids
    assert listing_b.id in response_ids
    assert listing_c.id not in response_ids
    assert listing_d.id not in response_ids


def test_filtering_property_by_min_and_max_square_footage(client, listing_a, listing_b, listing_c, listing_d, setup):
    response = client.get('/api/v1/listings/', {'square_footage_min': 2750, 'square_footage_max': 4050})

    response_data = response.json()

    assert response.status_code == 200
    assert len(response_data) == 3

    response_ids = [r.get('id') for r in response_data]

    assert listing_a.id in response_ids
    assert listing_b.id in response_ids
    assert listing_c.id in response_ids
    assert listing_d.id not in response_ids


def test_filtering_property_by_zip_code(client, listing_a, listing_b, listing_c, listing_d, setup):
    response = client.get('/api/v1/listings/', {'zip_code': '35801'})

    response_data = response.json()

    assert response.status_code == 200
    assert len(response_data) == 1

    response_ids = [r.get('id') for r in response_data]

    assert listing_a.id in response_ids
    assert listing_b.id not in response_ids
    assert listing_c.id not in response_ids
    assert listing_d.id not in response_ids


def test_showing_can_precede(listing_a, showing_a_1, format_string, realtor_a, setup):
    client = APIClient()

    realtor, _, _, token = realtor_a

    start_time = datetime.datetime(year=2019, month=1, day=1, hour=11)
    end_time = datetime.datetime(year=2019, month=1, day=1, hour=11, minute=30)

    data = {
        'agent': realtor.id,
        'start_time': start_time.strftime(format_string),
        'end_time': end_time.strftime(format_string)
    }

    response = perform_api_action(client.post, data, '/api/v1/listings/{}/showings/'.format(listing_a.id), token)

    assert response.status_code == status.HTTP_201_CREATED


def test_showing_can_follow(listing_a, showing_a_1, format_string, realtor_b, setup):
    client = APIClient()

    realtor, _, _, token = realtor_b

    start_time = datetime.datetime(year=2019, month=1, day=1, hour=12)
    end_time = datetime.datetime(year=2019, month=1, day=1, hour=12, minute=30)

    data = {
        'agent': realtor.id,
        'start_time': start_time.strftime(format_string),
        'end_time': end_time.strftime(format_string)
    }

    response = perform_api_action(client.post, data, '/api/v1/listings/{}/showings/'.format(listing_a.id), token)

    assert response.status_code == status.HTTP_201_CREATED


def test_showing_cannot_overlap_early(listing_a, showing_a_1, format_string, realtor_b, setup):
    client = APIClient()

    realtor, _, _, token = realtor_b

    start_time = datetime.datetime(year=2019, month=1, day=1, hour=11, minute=15)
    end_time = datetime.datetime(year=2019, month=1, day=1, hour=11, minute=45)

    data = {
        'agent': realtor.id,
        'start_time': start_time.strftime(format_string),
        'end_time': end_time.strftime(format_string)
    }

    response = perform_api_action(client.post, data, '/api/v1/listings/{}/showings/'.format(listing_a.id), token)

    assert response.status_code == status.HTTP_400_BAD_REQUEST


def test_showing_cannot_overlap_late(listing_a, showing_a_1, format_string, realtor_a, setup):
    client = APIClient()

    realtor, _, _, token = realtor_a

    start_time = datetime.datetime(year=2019, month=1, day=1, hour=11, minute=45)
    end_time = datetime.datetime(year=2019, month=1, day=1, hour=12, minute=15)

    data = {
        'agent': realtor.id,
        'start_time': start_time.strftime(format_string),
        'end_time': end_time.strftime(format_string)
    }

    response = perform_api_action(client.post, data, '/api/v1/listings/{}/showings/'.format(listing_a.id), token)

    assert response.status_code == status.HTTP_400_BAD_REQUEST


def test_showing_cannot_overlap_exact(listing_a, showing_a_1, format_string, realtor_a, setup):
    client = APIClient()

    realtor, _, _, token = realtor_a

    start_time = datetime.datetime(year=2019, month=1, day=1, hour=11, minute=30)
    end_time = datetime.datetime(year=2019, month=1, day=1, hour=12)

    data = {
        'agent': realtor.id,
        'start_time': start_time.strftime(format_string),
        'end_time': end_time.strftime(format_string)
    }

    response = perform_api_action(client.post, data, '/api/v1/listings/{}/showings/'.format(listing_a.id), token)

    assert response.status_code == status.HTTP_400_BAD_REQUEST


def test_showing_times_cannot_be_swapped(realtor_a, listing_a, format_string, setup):
    client = APIClient()

    realtor, _, _, token = realtor_a

    start_time = datetime.datetime(year=2019, month=1, day=1, hour=11, minute=30)
    end_time = datetime.datetime(year=2019, month=1, day=1, hour=11)

    data = {
        'agent': realtor.id,
        'start_time': start_time.strftime(format_string),
        'end_time': end_time.strftime(format_string)
    }

    response = perform_api_action(client.post, data, '/api/v1/listings/{}/showings/'.format(listing_a.id), token)

    assert response.status_code == status.HTTP_400_BAD_REQUEST


def test_showing_times_cannot_be_equal(realtor_a, listing_a, format_string, setup):
    client = APIClient()

    realtor, _, _, token = realtor_a

    start_time = datetime.datetime(year=2019, month=1, day=1, hour=11)
    end_time = datetime.datetime(year=2019, month=1, day=1, hour=11)

    data = {
        'agent': realtor.id,
        'start_time': start_time.strftime(format_string),
        'end_time': end_time.strftime(format_string)
    }

    response = perform_api_action(client.post, data, '/api/v1/listings/{}/showings/'.format(listing_a.id), token)

    assert response.status_code == status.HTTP_400_BAD_REQUEST


def test_user_can_retrieve_own_messages(realtor_a, setup):
    client = APIClient()

    realtor, _, _, token = realtor_a

    messages = UserMessage.objects.filter(user_id=realtor)

    response = perform_api_action(client.get, {}, '/api/v1/messages/', token)

    response_ids = [r.get('id') for r in response.json()]
    message_ids = [m.id for m in messages]

    assert response.status_code == status.HTTP_200_OK
    assert message_ids == response_ids


def test_user_can_retrieve_specific_message(realtor_a, setup):
    client = APIClient()

    realtor, _, _, token = realtor_a

    message = UserMessage.objects.filter(user_id=realtor).first()

    response = perform_api_action(client.get, {}, '/api/v1/messages/{}/'.format(message.id), token)

    assert response.status_code == status.HTTP_200_OK
    assert response.json().get('id') == message.id


def test_user_cannot_retrieve_other_messages(realtor_a, realtor_b, setup):
    client = APIClient()

    realtor, _, _, token = realtor_b

    messages = UserMessage.objects.filter(user_id=realtor)

    response = perform_api_action(client.get, {}, '/api/v1/messages/', token)

    response_ids = [r.get('id') for r in response.json()]
    message_ids = [m.id for m in messages]

    assert response.status_code == status.HTTP_200_OK
    assert message_ids == response_ids


def test_user_cannot_retrieve_other_specific_message(realtor_a, realtor_b, setup):
    client = APIClient()

    realtor, _, _, _ = realtor_a
    _, _, _, token = realtor_b

    message = UserMessage.objects.filter(user_id=realtor).first()

    response = perform_api_action(client.get, {}, '/api/v1/messages/{}/'.format(message.id), token)

    assert response.status_code == status.HTTP_404_NOT_FOUND


@pytest.mark.django_db
def test_unauthenticated_user_has_no_messages(client, setup):
    response: Response = client.get('/api/v1/messages/')
    assert response.status_code == 200
    assert response.json() == []


def test_realtor_can_add_nearby_attraction(realtor_a, listing_a, setup):
    client = APIClient()

    realtor, _, _, token = realtor_a

    data = {'name': 'Some Middle School', 'type': 'SCHOOL_MIDDLE'}

    response = perform_api_action(
        client.post,
        data,
        '/api/v1/listings/{}/property/{}/nearby_attractions/'.format(listing_a.id, listing_a.property.id),
        token
    )

    assert response.status_code == status.HTTP_201_CREATED

    assert response.json() == {**data}


def test_realtor_can_add_room(realtor_a, listing_a):
    client = APIClient()

    realtor, _, _, token = realtor_a

    data = {
        'name': 'Guest Kitchen',
        'type': 'KITCHEN',
        'description': 'Recently Updated, but kinda small',
        'square_footage': 12
    }

    response = perform_api_action(
        client.post,
        data,
        '/api/v1/listings/{}/property/{}/rooms/'.format(listing_a.id, listing_a.property.id),
        token
    )

    assert response.status_code == status.HTTP_201_CREATED

    assert response.json() == {**data}


def test_invalid_room_type_caught(realtor_a, listing_a):
    client = APIClient()

    realtor, _, _, token = realtor_a

    data = {
        'name': 'Parlor',
        'description': 'Who has these anymore?',
        'type': 'PARLOR'
    }

    response = perform_api_action(
        client.post,
        data,
        '/api/v1/listings/{}/property/{}/rooms/'.format(listing_a.id, listing_a.property.id),
        token
    )

    assert response.status_code == status.HTTP_400_BAD_REQUEST


def test_anyone_can_get_rooms(client, listing_a):
    response: Response = client.get(
        '/api/v1/listings/{}/property/{}/rooms/'.format(listing_a.id, listing_a.property.id)
    )

    assert response.status_code == status.HTTP_200_OK
    assert [r.get('id') for r in response.json()] == [r.id for r in listing_a.property.rooms.all()]


def test_anyone_can_get_iam_policy_statement(client, policy: Tuple[IAMPolicy, dict], setup):
    response: Response = client.get(
        '/api/v1/iam_policies/{}/statements/'.format(policy[0].id)
    )

    assert response.status_code == status.HTTP_200_OK
    assert [r.get('id') for r in response.json()] == [r.id for r in policy[0].statements.all()]


def test_admin_can_create_iam_policy_statement(client, admin_user, policy: Tuple[IAMPolicy, dict], setup):
    client = APIClient()

    realtor, token = admin_user

    data = {
        'notes': 'Just another action...',
        'actions': ['safe'],
        'effect': 'allow',
        'principals': [{'value': '*'}],
        'conditions': []
    }

    response = perform_api_action(
        client.post,
        data,
        '/api/v1/iam_policies/{}/statements/'.format(policy[0].id),
        token
    )

    assert response.status_code == status.HTTP_201_CREATED


def test_anyone_can_get_iam_policy_statement_principals(client, policy: Tuple[IAMPolicy, dict], setup):
    response: Response = client.get(
        '/api/v1/iam_policies/{}/statements/{}/principals/'.format(policy[0].id, policy[0].statements.first().id)
    )

    assert response.status_code == status.HTTP_200_OK
    assert [r.get('id') for r in response.json()] == [r.id for r in policy[0].statements.first().principals.all()]


def test_admin_can_create_iam_policy_statement_principal(client, admin_user, policy: Tuple[IAMPolicy, dict], setup):
    client = APIClient()

    realtor, token = admin_user

    data = {
        'value': 'group:plebes'
    }

    response = perform_api_action(
        client.post,
        data,
        '/api/v1/iam_policies/{}/statements/{}/principals/'.format(policy[0].id, policy[0].statements.first().id),
        token
    )

    assert response.status_code == status.HTTP_201_CREATED


def test_anyone_can_get_iam_policy_statement_conditions(client, policy: Tuple[IAMPolicy, dict], setup):
    response: Response = client.get(
        '/api/v1/iam_policies/{}/statements/{}/conditions/'.format(policy[0].id, policy[0].statements.first().id)
    )

    assert response.status_code == status.HTTP_200_OK
    assert [r.get('id') for r in response.json()] == [r.id for r in policy[0].statements.first().conditions.all()]


def test_admin_can_create_iam_policy_statement_condition(client, admin_user, policy: Tuple[IAMPolicy, dict], setup):
    client = APIClient()

    realtor, token = admin_user

    data = {
        'value': 'user_is_plebe'
    }

    response = perform_api_action(
        client.post,
        data,
        '/api/v1/iam_policies/{}/statements/{}/conditions/'.format(policy[0].id, policy[0].statements.first().id),
        token
    )

    assert response.status_code == status.HTTP_201_CREATED


def test_listings_path_generator():
    uuid = 'xxxxxxxx-xxxx-xxxx-xxxx-xxxxxxxxxxxx'
    filename = 'image.jpeg'

    uuid_mock = MagicMock()
    uuid_mock.return_value = uuid

    assert listing_path_generator(None, filename, uuid_mock) == 'listings/{}.jpeg'.format(uuid)
    assert uuid_mock.called_once()


def test_avatar_path_generator():
    uuid = 'xxxxxxxx-xxxx-xxxx-xxxx-xxxxxxxxxxxx'
    filename = 'image.jpeg'

    uuid_mock = MagicMock()
    uuid_mock.return_value = uuid

    assert avatar_path_generator(None, filename, uuid_mock) == 'avatars/{}.jpeg'.format(uuid)
    assert uuid_mock.called_once()


def test_mls_number_will_not_be_unique(realtor_a):
    _, agency, _, _ = realtor_a

    uuid_1 = UUID(hex='11111111-2222-3333-4444-555555555555')
    uuid_2 = UUID(hex='66666666-7777-8888-9999-000000000000')

    mls = MLSNumber.objects.create(agency_id=agency.id)
    mls.number = uuid_1.fields[-1]
    mls.save()

    with patch('uuid.uuid4') as mocked_uuid:
        mocked_uuid.side_effect = [uuid_1, uuid_1, uuid_2]

        new_mls = MLSNumber.objects.create(agency_id=agency.id)

        assert mocked_uuid.mock_has_calls([call(), call(), call()])
        assert new_mls.number == uuid_2.fields[-1]


def test_database_apps():
    assert DatabaseConfig.name == 'database'


def test_wsgi():
    with patch('django.core.wsgi.get_wsgi_application') as mocked_wsgi:
        mocked_wsgi.return_value = 'totally_the_right_type'

        from foundry_backend import wsgi

        assert mocked_wsgi.called_once()
        assert wsgi.application == 'totally_the_right_type'

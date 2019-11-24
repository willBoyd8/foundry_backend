import datetime
import logging

import pytest
from django.contrib.auth.models import User, Group
from rest_framework.authtoken.models import Token

from foundry_backend.api import startup
from foundry_backend.api.models import IAMPolicy, IAMPolicyStatement, IAMPolicyStatementPrincipal, \
    IAMPolicyStatementCondition
from foundry_backend.database import models
from foundry_backend.database.models import MLSNumber, Agency, Address, UserMessage


@pytest.fixture
def setup(db):
    startup.load_iam_policies(logging.getLogger('AccessPolicyManager'))


@pytest.fixture
def format_string():
    return '%Y-%m-%d %H:%M'


@pytest.fixture
def admin_user(db):
    # make the user and group, with a token
    user, _ = User.objects.get_or_create(username='admin', email='admin@email.com', password='password')
    token = Token.objects.create(user=user)

    user.is_staff = True
    user.is_superuser = True

    user.save()
    token.save()
    admin_group = Group.objects.get_or_create(name='admin')[0]
    admin_group.save()
    admin_group.user_set.add(user)
    admin_group.save()
    return user, token


@pytest.fixture
def realtor_a(db):
    address = Address(street_number='1234', street='Someplace Drive Road', postal_code='35801', locality='Huntsville',
                      state_code='AL', state='Alabama')
    address.save()
    agency = Agency.objects.create(name='Alpha Agency', phone='+18626405799',
                                   address=address)
    realtor = User.objects.create_user(username='realtor_a', first_name='Realtor', last_name='A',
                                       email='realtor_a@email.com', password='password')
    mls = MLSNumber.objects.create(user=realtor, agency=agency)
    token = Token.objects.create(user=realtor)

    agency.save()
    realtor.save()
    mls.save()
    token.save()

    _ = UserMessage.objects.create(
        user_id=realtor.id,
        message='Someone wants to see \'1600 Pennsylvania Avenue\'!',
        type='SHOWING'
    )

    _ = UserMessage.objects.create(
        user_id=realtor.id,
        message='On January 1st, 2020, 17 people viewed  \'1600 Pennsylvania Avenue\'!',
        type='HITS'
    )

    realtor_group = Group.objects.get_or_create(name='realtor')[0]
    realtor_group.save()

    realtor_group.user_set.add(realtor)
    realtor_group.save()

    return realtor, agency, mls, token


@pytest.fixture
def realtor_b(db):
    address = Address(street_number='5678', street='Someplace Drive Road', postal_code='35801', locality='Madison',
                      state_code='TX', state='Texas')
    address.save()
    agency = Agency.objects.create(name='Beta Agency', phone='+12025550143',
                                   address=address)
    realtor = User.objects.create_user(username='realtor_b', email='realtor_b@email.com', password='password')
    mls = MLSNumber.objects.create(user=realtor, agency=agency)
    token = Token.objects.create(user=realtor)

    agency.save()
    realtor.save()
    mls.save()
    token.save()

    _ = UserMessage.objects.create(
        user_id=realtor.id,
        message='Someone wants to see \'11 Wall Street\'!',
        type='SHOWING'
    )

    realtor_group = Group.objects.get_or_create(name='realtor')[0]
    realtor_group.save()

    realtor_group.user_set.add(realtor)
    realtor_group.save()

    return realtor, agency, mls, token


@pytest.fixture
def realtor_c(db, realtor_a):
    _, agency, _, _ = realtor_a
    realtor = User.objects.create_user(username='realtor_c', email='realtor_c@email.com', password='password')
    mls = MLSNumber.objects.create(user=realtor, agency=agency)
    token = Token.objects.create(user=realtor)

    agency.save()
    realtor.save()
    mls.save()
    token.save()

    realtor_group = Group.objects.get_or_create(name='realtor')[0]
    realtor_group.save()

    realtor_group.user_set.add(realtor)
    realtor_group.save()

    return realtor, agency, mls, token


@pytest.fixture
def listing_a(realtor_a):
    address = models.Address.objects.create(street_number='1516',
                                            street='Big Cove Road',
                                            postal_code='35801',
                                            locality='Huntsville',
                                            state_code='AL',
                                            state='Alabama')

    listing = models.Listing.objects.create(asking_price=500000, agent=realtor_a[2],
                                            description='Custom built home with lots of light and a beautiful treed '
                                                        'lot. Hardwoods in the formals plus a study & library that '
                                                        'open to a rear flagstone patio. Formerly owned by Dr. Wernher '
                                                        'von Braun.')

    prop = models.Property.objects.create(address=address, type='HOUSE', square_footage='2750', acreage=1.25,
                                          listing=listing)

    address.save()
    prop.save()
    listing.save()

    return listing


@pytest.fixture
def showing_a_1(listing_a, realtor_a):
    start_time = datetime.datetime(year=2019, month=1, day=1, hour=11, minute=30)
    end_time = datetime.datetime(year=2019, month=1, day=1, hour=12, minute=00)

    _, _, realtor, _ = realtor_a

    showing = models.Showing.objects.create(start_time=start_time,
                                            end_time=end_time,
                                            listing=listing_a,
                                            agent=realtor)

    return showing


@pytest.fixture
def listing_b(realtor_a):
    address = models.Address.objects.create(street_number='1234',
                                            street='Someplace Drive',
                                            postal_code='35802',
                                            locality='Huntsville',
                                            state_code='AL',
                                            state='Alabama')

    listing = models.Listing.objects.create(asking_price=600000, agent=realtor_a[2],
                                            description='It\'s nice and spacious...')

    prop = models.Property.objects.create(address=address, type='HOUSE', square_footage='3000', acreage=999.99,
                                          listing=listing)

    address.save()
    prop.save()
    listing.save()

    return listing


@pytest.fixture
def listing_c(realtor_a):
    address = models.Address.objects.create(street_number='2345',
                                            street='Someplace Drive',
                                            postal_code='35802',
                                            locality='Huntsville',
                                            state_code='AL',
                                            state='Alabama')

    listing = models.Listing.objects.create(asking_price=700000, agent=realtor_a[2],
                                            description='It\'s nice and spacious...')

    prop = models.Property.objects.create(address=address, type='APARTMENT', square_footage='4000', acreage=0,
                                          listing=listing)

    address.save()
    prop.save()
    listing.save()

    return listing


@pytest.fixture
def listing_d(realtor_a):
    address = models.Address.objects.create(street_number='3456',
                                            street='Someplace Drive',
                                            postal_code='35802',
                                            locality='Huntsville',
                                            state_code='AL',
                                            state='Alabama')

    listing = models.Listing.objects.create(asking_price=800000, agent=realtor_a[2],
                                            description='It\'s nice and spacious...')

    prop = models.Property.objects.create(address=address, type='HOUSE', square_footage='5000', acreage=0.25,
                                          listing=listing)

    address.save()
    prop.save()
    listing.save()

    return listing


@pytest.fixture
def listing_e(realtor_b):
    address = models.Address.objects.create(street_number='256',
                                            street='Someplace Drive',
                                            postal_code='35802',
                                            locality='Huntsville',
                                            state_code='AL',
                                            state='Alabama')

    listing = models.Listing.objects.create(
        asking_price=800000,
        agent=realtor_b[2],
        description='It\'s not for sale',
        open=False
    )

    prop = models.Property.objects.create(address=address, type='HOUSE', square_footage='5000', acreage=0.25,
                                          listing=listing)

    address.save()
    prop.save()
    listing.save()

    return listing


@pytest.fixture
def policy(db):
    policy = IAMPolicy.objects.create(name='an-example-policy', notes='Does some stuff')
    statement = IAMPolicyStatement.objects.create(notes='A policy', policy=policy,
                                                  actions=['list', 'retrieve'], effect='allow')
    principal = IAMPolicyStatementPrincipal.objects.create(statement=statement, value='*')
    condition = IAMPolicyStatementCondition.objects.create(statement=statement, value='true_is_not_false')

    policy.save()
    statement.save()
    principal.save()
    condition.save()

    data = dict(name='an-example-policy', notes='Does some stuff',
                statements=[
                    dict(notes='A policy', actions=['list', 'retrieve'], effect='allow',
                         principals=[dict(value='*')], conditions=[dict(value='true_is_not_false')])
                ])

    return policy, data

import pytest
from django.contrib.auth.models import User, Group
from rest_framework.test import APIRequestFactory

from foundry_backend.database.models import Agency, Address, MLSNumber


@pytest.fixture
def request_factory():
    return APIRequestFactory()


@pytest.fixture
def admin_user(db):
    admin_group: Group = Group.objects.get_or_create(name='admins')[0]
    user: User = User.objects.create(username='admin', password='password')
    admin_group.user_set.add(user)
    user.save()

    return user


@pytest.fixture
def piper_and_leaf(db):
    """
    Piper and Leaf

    2211 Seminole Dr SW
    Unit 151
    Huntsville, AL 35805
    United States
    """
    return (Address.objects.create(street_number='2211', street='Seminole Dr SW', locality='Huntsville',
                                   state='Alabama', state_code='AL', postal_code='35805'), '+12569299404')


@pytest.fixture
def honest_coffee_roasters(db):
    """
    Honest Coffee Roasters

    114 Clinton Ave E
    Unit 106
    Huntsville, AL  35801
    United States
    """
    return (Address.objects.create(street_number='114', street='Clinton Ave E', locality='Huntsville',
                                   state='Alabama', state_code='AL', postal_code='35801'), '+12569646993')


@pytest.fixture
def realtor_a(db, piper_and_leaf):

    agency: Agency = Agency(name='Alpha Realty', address=piper_and_leaf[0], phone=piper_and_leaf[1])
    user: User = User.objects.create(username='realtor_a', password='password')

    piper_and_leaf[0].save()
    agency.save()
    user.save()

    mls: MLSNumber = MLSNumber.objects.create(agency=agency, user=user)
    mls.save()

    return user


@pytest.fixture
def realtor_b(db, honest_coffee_roasters):
    agency: Agency = Agency(name='Beta Realty', address=honest_coffee_roasters[0], phone=honest_coffee_roasters[1])
    user: User = User.objects.create(username='realtor_b', password='password')

    honest_coffee_roasters[0].save()
    agency.save()
    user.save()

    mls: MLSNumber = MLSNumber.objects.create(agency=agency, user=user)
    mls.save()

    return user

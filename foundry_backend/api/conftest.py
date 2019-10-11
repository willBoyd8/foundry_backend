import pytest
from django.contrib.auth.models import User, Group
from requests_toolbelt.utils import user_agent
from rest_framework.authtoken.models import Token
from rest_framework.test import APIClient

from foundry_backend.database.models import MLSNumber, Agency


@pytest.fixture
def admin_user(db):
    # make the user and group, with a token
    user = User.objects.create_user(username='admin', email='admin@email.com', password='password')
    token = Token.objects.create(user=user)
    user.save()
    token.save()

    admin_group = Group.objects.get_or_create(name='admin')[0]
    admin_group.save()

    admin_group.user_set.add(user)
    admin_group.save()

    return user, token


@pytest.fixture
def realtor_a(db):
    agency = Agency.objects.create(name='Alpha Agency', address='Someplace Drive', phone='+18626405799')
    realtor = User.objects.create_user(username='realtor_a', email='realtor_a@email.com', password='password')
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
def realtor_b(db):
    agency = Agency.objects.create(name='Beta Agency', address='Someplace Road', phone='+12025550143')
    realtor = User.objects.create_user(username='realtor_b', email='realtor_b@email.com', password='password')
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

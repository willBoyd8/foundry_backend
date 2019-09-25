import pytest
from . import models


# Create your tests here.
@pytest.mark.django_db
def test_create_agency():
    name = 'Real Estate, Inc.'
    address = '1234 Road Street, City, ST, America'
    phone = '+41524204242'

    agency = models.Agency(name=name,
                           address=address,
                           phone=phone)
    assert agency.name == name
    assert agency.address == address
    assert agency.phone == phone



from django.db import models
from phonenumber_field.modelfields import PhoneNumberField
from address.models import AddressField


class Agency(models.Model):
    """
    Represents a real estate agency
    """
    name = models.CharField(max_length=50, unique=True)
    address = models.TextField(unique=True)
    phone = PhoneNumberField()


class MLSNumber(models.Model):
    """
    A realtor's MLS Number
    """
    number = models.SlugField(max_length=12, unique=True)
    agency = models.ForeignKey(Agency, on_delete=models.CASCADE)

from django.contrib.auth.models import User
from django.core.validators import MinValueValidator, MinLengthValidator, MaxLengthValidator, MaxValueValidator
from django.db import models
from phonenumber_field.modelfields import PhoneNumberField
import uuid
from rest_framework.exceptions import ValidationError


class UserMessage(models.Model):
    """
    Stores a message to a user
    """
    MESSAGE_TYPES = (
        ('HITS', 'Hit Count on a listing'),
        ('SHOWING', 'Request for a showing'),
        ('MISC', 'Misc.')
    )

    user = models.ForeignKey(User, related_name='messages', on_delete=models.CASCADE)
    message = models.TextField()
    type = models.CharField(max_length=10, choices=MESSAGE_TYPES)
    read = models.BooleanField(default=False, blank=True)


def avatar_path_generator(_, filename):
    extension = filename.split(".")[-1]
    return "avatars/{}.{}".format(uuid.uuid4(), extension)


class Avatar(models.Model):
    """
    A user avatar
    """
    avatar = models.ImageField(upload_to=avatar_path_generator)
    user = models.OneToOneField(User, on_delete=models.CASCADE)


class Address(models.Model):
    """
    An address entry
    """
    street_number = models.CharField(max_length=5)
    street = models.CharField(max_length=50)
    locality = models.CharField(max_length=50)
    postal_code = models.CharField(max_length=5, validators=[MinLengthValidator(5), MaxLengthValidator(5)])
    state = models.CharField(max_length=15)
    state_code = models.CharField(max_length=2, validators=[MinLengthValidator(2), MaxLengthValidator(2)])

    class Meta:
        unique_together = (('street_number', 'street', 'locality', 'postal_code', 'state_code'),)

    def to_dict(self):
        return {
            'locality': self.locality,
            'postal_code': self.postal_code,
            'state': self.state,
            'state_code': self.state_code,
            'street': self.street,
            'street_number': self.street_number
        }


class Agency(models.Model):
    """
    Represents a real estate agency
    """
    name = models.CharField(max_length=50, unique=True)
    address = models.ForeignKey(Address, on_delete=models.CASCADE)
    phone = PhoneNumberField()


class MLSNumber(models.Model):
    """
    A realtor's MLS Number
    """
    number = models.CharField(max_length=12, unique=True, blank=True)
    agency = models.ForeignKey(Agency, related_name='mls_numbers', on_delete=models.CASCADE)
    user = models.OneToOneField(User, related_name='mls_number', on_delete=models.CASCADE, null=True, unique=True)

    def _generate_number(self):
        """
        Generate a unique MLS number for a realtor

        MLS numbers are generated by creating a unique UUID v4 object
        and taking the "node" section (last 6 bytes).

        :return: a string ID, unique across cls.number
        """
        mls = uuid.uuid4()

        while self.__class__.objects.filter(number=mls.fields[-1]).exists():
            mls = uuid.uuid4()

        self.number = mls.fields[-1]

    def save(self, force_insert=False, force_update=False, using=None, update_fields=None):
        if not self.pk:
            self._generate_number()

        super().save(force_insert=force_insert, force_update=force_update, using=using, update_fields=update_fields)


class Listing(models.Model):
    """
    A listing of a house
    """
    asking_price = models.IntegerField(validators=[MinValueValidator(0)])
    description = models.TextField()
    agent = models.ForeignKey(MLSNumber, on_delete=models.CASCADE)


class ListingsHit(models.Model):
    """
    Stores a hit for a model
    """
    listing = models.ForeignKey(Listing, related_name='hits', on_delete=models.CASCADE)
    access_time = models.DateTimeField(auto_now_add=True)


def listing_path_generator(_, filename):
    extension = filename.split(".")[-1]
    return "listings/{}.{}".format(uuid.uuid4(), extension)


class ListingImage(models.Model):
    """
    An image of a listing
    """
    listing = models.ForeignKey(Listing, related_name='images', on_delete=models.CASCADE)
    image = models.ImageField(upload_to=listing_path_generator)
    description = models.TextField(null=True, blank=True)


class Property(models.Model):
    """
    A property model
    """
    PROPERTY_TYPES = (
        ('APARTMENT', 'Apartment'),
        ('CONDO', 'Condominium'),
        ('DUPLEX', 'Duplex Home'),
        ('HOUSE', 'Standalone House')
    )

    listing = models.OneToOneField(Listing, related_name='property', on_delete=models.CASCADE)
    address = models.ForeignKey(Address, on_delete=models.CASCADE)
    square_footage = models.IntegerField(validators=[MinValueValidator(0)])
    acreage = models.DecimalField(validators=[MinValueValidator(0), MaxValueValidator(999.99)],
                                  decimal_places=2, max_digits=5)
    type = models.CharField(max_length=12, choices=PROPERTY_TYPES)


class NearbyAttraction(models.Model):
    """
    A superclass for all the things near a property
    """
    NEARBY_ATTRACTION_TYPES = (
        ('SCHOOL_ELEM', 'Public Elementary School'),
        ('SCHOOL_MIDDLE', 'Public Middle School'),
        ('SCHOOL_HIGH', 'Public High School'),
        ('SCHOOL_PRIVATE', 'Private School'),
        ('SHOPPING', 'Shopping Area'),
        ('NEIGHBORHOOD', 'Neighborhood'),
        ('ENTERTAINMENT', 'Entertainment Area'),
    )

    properties = models.ManyToManyField(Property,  blank=True, related_name='nearby_attractions',
                                        through="NearbyAttractionPropertyConnector")
    name = models.CharField(max_length=50)
    type = models.CharField(max_length=15, choices=NEARBY_ATTRACTION_TYPES)


class NearbyAttractionPropertyConnector(models.Model):
    """
    Connect properties to nearby schools
    """
    attraction = models.ForeignKey(NearbyAttraction, on_delete=models.CASCADE)
    property = models.ForeignKey(Property, on_delete=models.CASCADE)

    class Meta:
        unique_together = (('attraction', 'property'),)


class Room(models.Model):
    """
    An individual room in the house
    """
    ROOM_TYPES = (
        ('BEDROOM', 'Bedroom'),
        ('BATHROOM', 'Bathroom'),
        ('HALF_BATHROOM', '1/2 bathroom'),
        ('KITCHEN', 'Kitchen'),
        ('DINING', 'Dining Room'),
        ('OFFICE', 'Office'),
        ('DEN', 'Den'),
        ('LIVING', 'Living Room'),
        ('FAMILY', 'Family Room'),
        ('GARAGE', 'Garage'),
        ('CAR_PORT', 'Car Port'),
        ('RECREATION', 'Recreational Room')
    )

    description = models.TextField(null=True, blank=True)
    name = models.CharField(max_length=25)
    property = models.ForeignKey(Property, related_name='rooms', on_delete=models.CASCADE)
    type = models.CharField(max_length=15, choices=ROOM_TYPES)

    class Meta:
        unique_together = (('name', 'property'),)


class HomeAlarm(models.Model):
    """
    Info for the homeowner's alarm and security info
    """
    property = models.OneToOneField(Property, related_name='home_alarm', on_delete=models.CASCADE)
    arm_code = models.CharField(max_length=50)
    disarm_code = models.CharField(max_length=50)
    password = models.CharField(max_length=50)
    notes = models.TextField()


class Showing(models.Model):
    """
    A showing of a property
    """
    start_time = models.DateTimeField()
    end_time = models.DateTimeField()
    agent = models.ForeignKey(MLSNumber, on_delete=models.CASCADE)
    listing = models.ForeignKey(Listing, on_delete=models.CASCADE)

    def save(self, force_insert=False, force_update=False, using=None,
             update_fields=None):

        if self.start_time > self.end_time:
            raise ValidationError({'start_time': "\'start_time\' cannot be less than \'end_time\'.",
                                   'end_time': "\'start_time\' cannot be greater than \'end_time\'."})

        if self.start_time == self.end_time:
            raise ValidationError("\'start_time\' cannot equal \'end_time\'.")

        query = Showing.objects.exclude(id=self.id).filter(listing=self.listing).filter(
                # Preceding overlap
                models.Q(start_time__gte=self.start_time, start_time__lt=self.end_time, end_time__gte=self.end_time) |
                # Following overlap
                models.Q(end_time__gt=self.start_time, start_time__lte=self.start_time)
        )

        if query.exists():
            conflicting_listing = query.get()
            raise ValidationError("The time range conflicts with a showing from {} to {}".format(
                conflicting_listing.start_time, conflicting_listing.end_time)
            )

        super().save(force_insert=force_insert, force_update=force_update, using=using, update_fields=update_fields)

from django.core.validators import RegexValidator
from django.db import models
from django.contrib.auth.models import User
import datetime
import uuid

phone_regex = RegexValidator(regex=r'^\+?1?\d{9,15}$', message="Phone number must be entered in the format: '+999999999'. Up to 15 digits allowed.")


class Offer(models.Model):

    YEAR_CHOICES = []
    for r in range(1901, (datetime.datetime.now().year + 1)):
        YEAR_CHOICES.append((r, r))

    offer_id = models.UUIDField(primary_key=True, default=uuid.uuid1, editable=False)
    owner = models.ForeignKey(User, on_delete=models.CASCADE)
    make = models.CharField(max_length=20)
    model = models.CharField(max_length=20)
    engine_type = models.CharField(max_length=20)
    engine_capacity = models.CharField(max_length=4)
    body_type = models.CharField(max_length=20)
    production_year = models.IntegerField(choices=YEAR_CHOICES, default=datetime.datetime.now().year)
    description = models.TextField(default=None, blank=True)
    price = models.DecimalField(max_digits=6, decimal_places=2)
    created = models.DateField(auto_now_add=True)
    phone_number = models.CharField(validators=[phone_regex], max_length=17, blank=False)
    # image = models.FilePathField


class Manufacturer(models.Model):
    make = models.CharField(max_length=50)

    def __str__(self):
        return self.make


class BodyType(models.Model):
    body_type = models.CharField(max_length=20, blank=False)

    def __str__(self):
        return self.body_type


class EngineType(models.Model):
    engine_type = models.CharField(max_length=20, blank=False, unique=True)

    def __str__(self):
        return self.engine_type


class EngineCapacity(models.Model):
    engine_capacity = models.FloatField(blank=False, unique=True)

    def __str__(self):
        return str(self.engine_capacity)


class Contractor(models.Model):

    title = models.CharField(max_length=100, blank=False)
    street = models.TextField(max_length=100, blank=False)
    city = models.CharField(max_length=20, blank=False)
    country = models.CharField(max_length=40, blank=False)
    email = models.EmailField(blank=True)
    status = models.BooleanField(default=False)

    phone_number = models.CharField(validators=[phone_regex], max_length=17, blank=True)


class Country(models.Model):
    country = models.CharField(max_length=40, blank=False)


class City(models.Model):
    city = models.CharField(max_length=20, blank=False)
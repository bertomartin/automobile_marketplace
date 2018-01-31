from django.core.validators import RegexValidator
from django.db import models
from django.contrib.auth.models import AbstractUser
import datetime
import uuid
phone_regex = RegexValidator(regex=r'^\+?1?\d{9,15}$', message="Phone number must be entered in the format: '+999999999'. Up to 15 digits allowed.")


class User(AbstractUser):
    is_customer = models.BooleanField(default=False)
    is_contractor = models.BooleanField(default=False)


class Customer(models.Model):
    user = models.OneToOneField(User, related_name="customer_user", on_delete=models.CASCADE, primary_key=True)
    name = models.CharField(max_length=30, blank=True)
    email = models.EmailField(blank=True)
    phone_number = models.CharField(validators=[phone_regex], max_length=17, blank=True)


class Contractor(models.Model):
    user = models.OneToOneField(User, related_name="contractor_user", on_delete=models.CASCADE, primary_key=True)

    title = models.CharField(max_length=100, blank=False)
    street = models.CharField(max_length=100, blank=False)
    city = models.CharField(max_length=20, blank=False)
    country = models.CharField(max_length=40, blank=False)
    email = models.EmailField(blank=True)
    status = models.BooleanField(default=False)
    phone_number = models.CharField(validators=[phone_regex], max_length=17, blank=True)

    def __str__(self):
        return str(self.title)


class Currency(models.Model):
    currency = models.CharField(max_length=10)
    currency_abbr = models.CharField(max_length=5)


class Manufacturer(models.Model):
    make = models.CharField(max_length=50, unique=True)

    def __str__(self):
        return self.make


class Series(models.Model):

    series = models.CharField(max_length=20, unique=True)
    make_fk = models.ForeignKey(Manufacturer, on_delete=models.CASCADE)

    def __str__(self):
        return self.series


class BodyType(models.Model):
    body_type = models.CharField(max_length=20, unique=True, blank=False)

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


class Post(models.Model):

    YEAR_CHOICES = []
    for r in range(1901, (datetime.datetime.now().year + 1)):
        YEAR_CHOICES.append((r, r))

    offer_id = models.UUIDField(primary_key=True, default=uuid.uuid1, editable=False)
    owner = models.ForeignKey(User, on_delete=models.CASCADE)
    make = models.ForeignKey(Manufacturer, on_delete=models.SET_NULL, null=True)
    model = models.ForeignKey(Series, on_delete=models.SET_NULL, null=True)
    engine_type = models.ForeignKey(EngineType, on_delete=models.SET_NULL, null=True)
    engine_capacity = models.ForeignKey(EngineCapacity, on_delete=models.SET_NULL, null=True)
    body_type = models.ForeignKey(BodyType, on_delete=models.SET_NULL, null=True)
    production_year = models.IntegerField(choices=YEAR_CHOICES, default=datetime.datetime.now().year)
    description = models.TextField(default=None, blank=True)
    price = models.PositiveIntegerField(blank=None)
    created = models.DateField(auto_now_add=True)
    contact_person = models.CharField(max_length=40, blank=False)
    # currency = models.ForeignKey(Currency, on_delete=models.CASCADE)
    phone_number = models.CharField(validators=[phone_regex], max_length=17, blank=False)

    def __str__(self):
        return ('Make: ' + str(self.make) +
                ' Model: ' + str(self.model) +
                ' Year: ' + str(self.production_year) +
                ' Price: ' + str(self.price) + '£')


class InspectionRequest(models.Model):

    status = models.BooleanField(default=False)
    corresponding_post = models.ForeignKey(Post, on_delete=models.CASCADE)
    responsible_contractor = models.ForeignKey(Contractor, on_delete=models.CASCADE)
    requesting_customer = models.ForeignKey(Customer, related_name="requesting_customer", on_delete=models.CASCADE)
    details = models.TextField(blank=True)
    date_created = models.DateField(auto_now_add=True)
    date_resolved = models.DateField(null=True)


class Image(models.Model):
    post = models.ForeignKey(Post, on_delete=models.CASCADE)
    title = models.CharField(max_length=255, blank=True)
    image = models.FileField(upload_to='images/')


class Country(models.Model):
    country = models.CharField(max_length=40, blank=False)


class City(models.Model):
    city = models.CharField(max_length=20, blank=False)




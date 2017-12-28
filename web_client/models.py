from django.db import models
from django.contrib.auth.models import User
import datetime


class Offer(models.Model):

    YEAR_CHOICES = []
    for r in range(1901, (datetime.datetime.now().year + 1)):
        YEAR_CHOICES.append((r, r))

    owner = models.ForeignKey(User, on_delete=models.CASCADE)
    make = models.CharField(max_length=20)
    model = models.CharField(max_length=20)
    engine_type = models.CharField(max_length=20)
    engine_capacity = models.CharField(max_length=4)
    body_type = models.CharField(max_length=20)
    production_year = models.IntegerField(choices=YEAR_CHOICES, default=datetime.datetime.now().year)
    description = models.TextField(default=None, blank=True)
    price = models.DecimalField(max_digits=6, decimal_places=2)
    # image = models.FilePathField


class Manufacturer(models.Model):
    make = models.CharField(max_length=50)

    def __str__(self):
        return self.make


class BodyTypes(models.Model):
    body_type = models.CharField(max_length=20, blank=False)

    def __str__(self):
        return self.body_type


class EngineTypes(models.Model):
    engine_type = models.CharField(max_length=20, blank=False, unique=True)

    def __str__(self):
        return self.engine_type


class EngineCapacities(models.Model):
    engine_capacity = models.FloatField(blank=False, unique=True)

    def __str__(self):
        return str(self.engine_capacity)

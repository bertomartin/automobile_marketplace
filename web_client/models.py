from django.db import models
from django.core.urlresolvers import reverse


class Offer(models.Model):
    # TODO: each field should be a foreign key to list of related values
    make = models.CharField(max_length=20)
    model = models.CharField(max_length=20)
    engine = models.CharField(max_length=20)
    body_type = models.CharField(max_length=20)
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
        return self.engine_capacity

from django.db import models
from django.core.urlresolvers import reverse


class Offer(models.Model):
    # TODO: each field should be a foreign key to list of related values
    make = models.CharField(max_length=20)
    model = models.CharField(max_length=20)
    engine = models.CharField(max_length=20)
    body_type = models.CharField(max_length=20)
    # image = models.FilePathField

    def get_absolute_url(self):
        return reverse('homepage')


class BodyTypes(models.Model):
    body_type = models.CharField(max_length=20, blank=False)


class EngineTypes(models.Model):
    engine_type = models.CharField(max_length=20, blank=False, unique=True)


class EngineCapacities(models.Model):
    engine_capacity = models.FloatField(blank=False, unique=True)

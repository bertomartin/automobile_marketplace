from django.db import models
from django.core.urlresolvers import reverse


class Offer(models.Model):
    make = models.CharField(max_length=20)
    model = models.CharField(max_length=20)
    engine = models.CharField(max_length=20)
    body_type = models.CharField(max_length=20)
    # image = models.FilePathField

    def get_absolute_url(self):
        return reverse('homepage')

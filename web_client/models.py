from django.db import models


class Offer(models.Model):
    make = models.CharField
    model = models.CharField
    engine = models.CharField
    body_type = models.CharField
    # image = models.FilePathField

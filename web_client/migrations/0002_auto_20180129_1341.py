# -*- coding: utf-8 -*-
# Generated by Django 1.11 on 2018-01-29 13:41
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('web_client', '0001_initial'),
    ]

    operations = [
        migrations.AlterField(
            model_name='bodytype',
            name='body_type',
            field=models.CharField(max_length=20, unique=True),
        ),
    ]

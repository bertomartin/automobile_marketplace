# -*- coding: utf-8 -*-
# Generated by Django 1.11 on 2018-01-02 22:25
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('web_client', '0002_auto_20180102_2021'),
    ]

    operations = [
        migrations.AlterField(
            model_name='offer',
            name='price',
            field=models.PositiveIntegerField(blank=None),
        ),
    ]

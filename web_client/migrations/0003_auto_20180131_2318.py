# -*- coding: utf-8 -*-
# Generated by Django 1.11 on 2018-01-31 23:18
from __future__ import unicode_literals

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('web_client', '0002_auto_20180130_2109'),
    ]

    operations = [
        migrations.AlterField(
            model_name='inspectionrequest',
            name='requesting_customer',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='requesting_customer', to='web_client.Customer'),
        ),
    ]

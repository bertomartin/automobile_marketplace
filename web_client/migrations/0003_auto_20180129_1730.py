# -*- coding: utf-8 -*-
# Generated by Django 1.11 on 2018-01-29 17:30
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('web_client', '0002_auto_20180129_1341'),
    ]

    operations = [
        migrations.RenameField(
            model_name='image',
            old_name='referencing_offer',
            new_name='post',
        ),
        migrations.AddField(
            model_name='image',
            name='title',
            field=models.CharField(blank=True, max_length=255),
        ),
        migrations.AlterField(
            model_name='image',
            name='image',
            field=models.FileField(upload_to='images/'),
        ),
    ]

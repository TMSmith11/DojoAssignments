# -*- coding: utf-8 -*-
# Generated by Django 1.11.5 on 2017-10-28 18:22
from __future__ import unicode_literals

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('travel', '0002_destinationmanager'),
    ]

    operations = [
        migrations.DeleteModel(
            name='DestinationManager',
        ),
        migrations.RemoveField(
            model_name='destination',
            name='name',
        ),
    ]

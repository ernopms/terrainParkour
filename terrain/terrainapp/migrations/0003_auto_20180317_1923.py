# -*- coding: utf-8 -*-
# Generated by Django 1.11.1 on 2018-03-18 02:23
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('terrainapp', '0002_auto_20180317_1418'),
    ]

    operations = [
        migrations.AlterField(
            model_name='tixtransaction',
            name='day',
            field=models.DateField(blank=True, default=None),
        ),
    ]

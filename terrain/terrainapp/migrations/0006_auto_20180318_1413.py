# -*- coding: utf-8 -*-
# Generated by Django 1.11.1 on 2018-03-18 21:13
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('terrainapp', '0005_auto_20180318_1335'),
    ]

    operations = [
        migrations.AlterField(
            model_name='tixtransaction',
            name='transactionday',
            field=models.DateField(blank=True, default=None, null=True),
        ),
    ]

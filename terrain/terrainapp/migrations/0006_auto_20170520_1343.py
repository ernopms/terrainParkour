# -*- coding: utf-8 -*-
# Generated by Django 1.11.1 on 2017-05-20 20:43
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('terrainapp', '0005_run_rank'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='run',
            name='rank',
        ),
        migrations.AddField(
            model_name='bestrun',
            name='rank',
            field=models.IntegerField(blank=True, null=True),
        ),
    ]

# -*- coding: utf-8 -*-
# Generated by Django 1.11.1 on 2018-03-18 19:36
from __future__ import unicode_literals

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('terrainapp', '0003_auto_20180318_0031'),
    ]

    operations = [
        migrations.CreateModel(
            name='BadgeGrant',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('created', models.DateTimeField(auto_now_add=True)),
                ('updated', models.DateTimeField(auto_now=True)),
                ('badge', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='badgegrants', to='terrainapp.Badge')),
                ('user', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='badgegrants', to='terrainapp.RobloxUser')),
            ],
            options={
                'db_table': 'badgegrant',
            },
        ),
    ]

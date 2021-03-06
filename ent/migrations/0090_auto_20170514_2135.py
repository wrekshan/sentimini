# -*- coding: utf-8 -*-
# Generated by Django 1.9.7 on 2017-05-14 21:35
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('ent', '0089_auto_20170203_2104'),
    ]

    operations = [
        migrations.AddField(
            model_name='timing',
            name='default_timing',
            field=models.BooleanField(default=False),
        ),
        migrations.AddField(
            model_name='timing',
            name='fuzzy_denomination_start',
            field=models.CharField(default='', max_length=160),
        ),
        migrations.AddField(
            model_name='timing',
            name='iti_noise_start',
            field=models.IntegerField(blank=True, null=True),
        ),
        migrations.AddField(
            model_name='timing',
            name='iti_raw_start',
            field=models.IntegerField(blank=True, null=True),
        ),
    ]

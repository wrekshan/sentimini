# -*- coding: utf-8 -*-
# Generated by Django 1.9.7 on 2017-01-19 17:17
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('ent', '0072_timing_repeat'),
    ]

    operations = [
        migrations.AddField(
            model_name='actualtext',
            name='time_reponse',
            field=models.DateTimeField(blank=True, null=True),
        ),
        migrations.AddField(
            model_name='actualtext',
            name='time_sent',
            field=models.DateTimeField(blank=True, null=True),
        ),
    ]
# -*- coding: utf-8 -*-
# Generated by Django 1.9.7 on 2016-09-22 05:10
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('ent', '0066_actualtextltm_time_to_send_circa'),
    ]

    operations = [
        migrations.AddField(
            model_name='actualtextltm',
            name='time_to_send_day',
            field=models.CharField(default='', max_length=160, null=True),
        ),
    ]

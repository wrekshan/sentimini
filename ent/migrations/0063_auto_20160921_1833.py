# -*- coding: utf-8 -*-
# Generated by Django 1.9.7 on 2016-09-21 18:33
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('ent', '0062_actualtextstm_time_to_add'),
    ]

    operations = [
        migrations.AddField(
            model_name='actualtextltm',
            name='response_time',
            field=models.IntegerField(default=0),
        ),
        migrations.AddField(
            model_name='actualtextstm',
            name='response_time',
            field=models.IntegerField(default=0),
        ),
    ]

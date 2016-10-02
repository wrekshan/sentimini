# -*- coding: utf-8 -*-
# Generated by Django 1.9.7 on 2016-08-08 21:15
from __future__ import unicode_literals

from decimal import Decimal
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('ent', '0024_auto_20160804_1827'),
    ]

    operations = [
        migrations.AddField(
            model_name='usersetting',
            name='exp_response_rate',
            field=models.DecimalField(decimal_places=2, default=Decimal('0.6'), max_digits=3),
        ),
        migrations.AddField(
            model_name='usersetting',
            name='exp_response_time_avg',
            field=models.IntegerField(default=5),
        ),
        migrations.AddField(
            model_name='usersetting',
            name='exp_response_time_max',
            field=models.IntegerField(default=60),
        ),
        migrations.AddField(
            model_name='usersetting',
            name='exp_response_time_min',
            field=models.IntegerField(default=1),
        ),
        migrations.AddField(
            model_name='usersetting',
            name='time_to_declare_lost',
            field=models.IntegerField(default=61),
        ),
    ]

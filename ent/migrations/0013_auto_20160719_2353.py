# -*- coding: utf-8 -*-
# Generated by Django 1.9.7 on 2016-07-19 23:53
from __future__ import unicode_literals

import datetime
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('ent', '0012_entry_begin_date'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='entry',
            name='begin_date',
        ),
        migrations.AddField(
            model_name='usersetting',
            name='begin_date',
            field=models.DateTimeField(default=datetime.datetime(2000, 1, 1, 0, 0)),
        ),
    ]

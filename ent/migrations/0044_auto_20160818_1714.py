# -*- coding: utf-8 -*-
# Generated by Django 1.9.7 on 2016-08-18 17:14
from __future__ import unicode_literals

import datetime
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('ent', '0043_auto_20160818_1547'),
    ]

    operations = [
        migrations.AddField(
            model_name='usergenpromptfixed',
            name='date_begin',
            field=models.DateTimeField(blank=True, default=datetime.datetime.now),
        ),
        migrations.AddField(
            model_name='usergenpromptfixed',
            name='date_end',
            field=models.DateTimeField(default=datetime.datetime(2100, 1, 1, 0, 0)),
        ),
    ]
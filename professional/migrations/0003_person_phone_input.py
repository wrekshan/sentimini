# -*- coding: utf-8 -*-
# Generated by Django 1.9.7 on 2017-07-04 17:02
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('professional', '0002_auto_20170704_1659'),
    ]

    operations = [
        migrations.AddField(
            model_name='person',
            name='phone_input',
            field=models.CharField(default='', max_length=16),
        ),
    ]

# -*- coding: utf-8 -*-
# Generated by Django 1.9.7 on 2017-01-18 20:01
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('ent', '0069_auto_20170118_0410'),
    ]

    operations = [
        migrations.AddField(
            model_name='timing',
            name='hour_end_value',
            field=models.IntegerField(blank=True, null=True),
        ),
        migrations.AddField(
            model_name='timing',
            name='hour_start_value',
            field=models.IntegerField(blank=True, null=True),
        ),
    ]
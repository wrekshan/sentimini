# -*- coding: utf-8 -*-
# Generated by Django 1.9.7 on 2016-08-19 01:17
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('ent', '0044_auto_20160818_1714'),
    ]

    operations = [
        migrations.AddField(
            model_name='usergenpromptfixed',
            name='repeat_denomination',
            field=models.CharField(blank=True, default='day', max_length=100),
        ),
        migrations.AddField(
            model_name='usergenpromptfixed',
            name='repeat_number',
            field=models.IntegerField(default='1'),
        ),
    ]
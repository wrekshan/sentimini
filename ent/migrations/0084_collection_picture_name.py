# -*- coding: utf-8 -*-
# Generated by Django 1.9.7 on 2017-01-31 20:21
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('ent', '0083_possibletext_date_scheduled'),
    ]

    operations = [
        migrations.AddField(
            model_name='collection',
            name='picture_name',
            field=models.CharField(default='', max_length=160),
        ),
    ]

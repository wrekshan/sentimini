# -*- coding: utf-8 -*-
# Generated by Django 1.9.7 on 2017-01-22 18:29
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('ent', '0079_auto_20170122_0651'),
    ]

    operations = [
        migrations.AddField(
            model_name='possibletext',
            name='active',
            field=models.BooleanField(default=True),
        ),
    ]

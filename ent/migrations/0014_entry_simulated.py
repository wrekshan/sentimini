# -*- coding: utf-8 -*-
# Generated by Django 1.9.7 on 2016-07-20 04:13
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('ent', '0013_auto_20160719_2353'),
    ]

    operations = [
        migrations.AddField(
            model_name='entry',
            name='simulated',
            field=models.IntegerField(default=0),
        ),
    ]
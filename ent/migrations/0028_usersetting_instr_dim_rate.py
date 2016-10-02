# -*- coding: utf-8 -*-
# Generated by Django 1.9.7 on 2016-08-09 17:43
from __future__ import unicode_literals

import django.core.validators
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('ent', '0027_prompttext'),
    ]

    operations = [
        migrations.AddField(
            model_name='usersetting',
            name='instr_dim_rate',
            field=models.IntegerField(default=90, validators=[django.core.validators.MinValueValidator(0), django.core.validators.MaxValueValidator(100)]),
        ),
    ]

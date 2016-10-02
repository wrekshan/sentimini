# -*- coding: utf-8 -*-
# Generated by Django 1.9.7 on 2016-09-16 17:12
from __future__ import unicode_literals

import django.core.validators
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('ent', '0055_auto_20160910_0410'),
    ]

    operations = [
        migrations.AlterField(
            model_name='usersetting',
            name='user_generated_prompt_rate',
            field=models.IntegerField(default=80, validators=[django.core.validators.MinValueValidator(0), django.core.validators.MaxValueValidator(100)]),
        ),
    ]
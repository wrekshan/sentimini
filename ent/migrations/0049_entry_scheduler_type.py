# -*- coding: utf-8 -*-
# Generated by Django 1.9.7 on 2016-08-24 20:01
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('ent', '0048_usergenpromptfixed_hr_range'),
    ]

    operations = [
        migrations.AddField(
            model_name='entry',
            name='scheduler_type',
            field=models.CharField(default='System', max_length=160),
        ),
    ]
# -*- coding: utf-8 -*-
# Generated by Django 1.9.7 on 2016-07-18 17:57
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('ent', '0009_auto_20160715_2207'),
    ]

    operations = [
        migrations.AlterField(
            model_name='entry',
            name='prompt',
            field=models.CharField(default='', max_length=160),
        ),
    ]
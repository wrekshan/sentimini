# -*- coding: utf-8 -*-
# Generated by Django 1.9.7 on 2017-05-23 22:35
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('ent', '0093_auto_20170517_0531'),
    ]

    operations = [
        migrations.AddField(
            model_name='collection',
            name='author',
            field=models.CharField(default='', max_length=500),
        ),
        migrations.AddField(
            model_name='collection',
            name='long_description',
            field=models.CharField(default='', max_length=3000),
        ),
    ]

# -*- coding: utf-8 -*-
# Generated by Django 1.9.7 on 2016-10-07 16:42
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('ent', '0015_auto_20161007_1626'),
    ]

    operations = [
        migrations.AlterField(
            model_name='experiencesetting',
            name='text_set',
            field=models.CharField(default='', max_length=30, null=True),
        ),
    ]

# -*- coding: utf-8 -*-
# Generated by Django 1.9.7 on 2016-10-14 21:36
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('ent', '0025_auto_20161011_1643'),
    ]

    operations = [
        migrations.AddField(
            model_name='experiencesetting',
            name='unique_text_set',
            field=models.CharField(default='', max_length=30, null=True),
        ),
    ]

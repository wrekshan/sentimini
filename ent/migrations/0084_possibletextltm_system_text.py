# -*- coding: utf-8 -*-
# Generated by Django 1.9.7 on 2016-10-01 15:59
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('ent', '0083_actualtextstm_system_text'),
    ]

    operations = [
        migrations.AddField(
            model_name='possibletextltm',
            name='system_text',
            field=models.IntegerField(default=0),
        ),
    ]
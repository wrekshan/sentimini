# -*- coding: utf-8 -*-
# Generated by Django 1.9.7 on 2016-10-29 21:11
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('ent', '0047_possibletextltm_feed_name'),
    ]

    operations = [
        migrations.AddField(
            model_name='possibletextltm',
            name='feed_type',
            field=models.CharField(default='user', max_length=120, null=True),
        ),
    ]

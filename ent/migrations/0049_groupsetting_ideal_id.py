# -*- coding: utf-8 -*-
# Generated by Django 1.9.7 on 2016-10-31 16:41
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('ent', '0048_possibletextltm_feed_type'),
    ]

    operations = [
        migrations.AddField(
            model_name='groupsetting',
            name='ideal_id',
            field=models.IntegerField(default=0),
        ),
    ]

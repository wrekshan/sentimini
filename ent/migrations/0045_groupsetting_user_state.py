# -*- coding: utf-8 -*-
# Generated by Django 1.9.7 on 2016-10-29 14:42
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('ent', '0044_auto_20161029_1436'),
    ]

    operations = [
        migrations.AddField(
            model_name='groupsetting',
            name='user_state',
            field=models.CharField(default='activate', max_length=100),
        ),
    ]

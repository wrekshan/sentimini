# -*- coding: utf-8 -*-
# Generated by Django 1.9.7 on 2016-10-07 06:52
from __future__ import unicode_literals

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('ent', '0008_auto_20161007_0618'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='usersetting',
            name='dead_begin',
        ),
        migrations.RemoveField(
            model_name='usersetting',
            name='dead_end',
        ),
    ]

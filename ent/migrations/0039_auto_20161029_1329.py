# -*- coding: utf-8 -*-
# Generated by Django 1.9.7 on 2016-10-29 13:29
from __future__ import unicode_literals

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('ent', '0038_auto_20161029_1326'),
    ]

    operations = [
        migrations.RenameField(
            model_name='possibletextstm',
            old_name='text_type',
            new_name='feed_type',
        ),
    ]

# -*- coding: utf-8 -*-
# Generated by Django 1.9.7 on 2017-07-06 15:41
from __future__ import unicode_literals

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('ent', '0129_actualtext_original_text'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='actualtext',
            name='original_text',
        ),
    ]

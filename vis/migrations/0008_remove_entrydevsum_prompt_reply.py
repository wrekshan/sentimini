# -*- coding: utf-8 -*-
# Generated by Django 1.9.7 on 2016-07-17 17:56
from __future__ import unicode_literals

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('vis', '0007_entrydevsum'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='entrydevsum',
            name='prompt_reply',
        ),
    ]

# -*- coding: utf-8 -*-
# Generated by Django 1.9.7 on 2016-10-02 00:31
from __future__ import unicode_literals

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('scaffold', '0029_auto_20161001_0501'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='blog',
            name='tags',
        ),
    ]

# -*- coding: utf-8 -*-
# Generated by Django 1.9.7 on 2016-10-11 16:43
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('ent', '0024_auto_20161011_0523'),
    ]

    operations = [
        migrations.AlterField(
            model_name='usersetting',
            name='active_experiences',
            field=models.CharField(default='', max_length=5000, null=True),
        ),
    ]

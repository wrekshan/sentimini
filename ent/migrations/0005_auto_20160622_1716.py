# -*- coding: utf-8 -*-
# Generated by Django 1.9.7 on 2016-06-22 17:16
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('ent', '0004_remove_usersetting_intensive_period_on'),
    ]

    operations = [
        migrations.AlterField(
            model_name='usergenprompt',
            name='show_user',
            field=models.BooleanField(default=False),
        ),
    ]

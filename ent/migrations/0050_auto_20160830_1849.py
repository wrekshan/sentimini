# -*- coding: utf-8 -*-
# Generated by Django 1.9.7 on 2016-08-30 18:49
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('ent', '0049_entry_scheduler_type'),
    ]

    operations = [
        migrations.AlterField(
            model_name='usersetting',
            name='sleep_duration',
            field=models.IntegerField(default=8),
        ),
    ]
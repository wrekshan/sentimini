# -*- coding: utf-8 -*-
# Generated by Django 1.9.7 on 2016-07-18 16:32
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('vis', '0014_auto_20160718_1605'),
    ]

    operations = [
        migrations.AddField(
            model_name='entrydev',
            name='time_to_send_circa',
            field=models.CharField(default='AM', max_length=160, null=True),
        ),
        migrations.AddField(
            model_name='entrydevsum',
            name='time_to_send_circa',
            field=models.CharField(default='AM', max_length=160, null=True),
        ),
    ]
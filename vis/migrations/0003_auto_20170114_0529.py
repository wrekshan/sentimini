# -*- coding: utf-8 -*-
# Generated by Django 1.9.7 on 2017-01-14 05:29
from __future__ import unicode_literals

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('vis', '0002_auto_20161029_1314'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='emotiontoshow',
            name='user',
        ),
        migrations.RemoveField(
            model_name='entrydev',
            name='user',
        ),
        migrations.RemoveField(
            model_name='entrydevsum',
            name='user',
        ),
        migrations.RemoveField(
            model_name='usersettingdev',
            name='user',
        ),
        migrations.DeleteModel(
            name='EmotionToShow',
        ),
        migrations.DeleteModel(
            name='EntryDEV',
        ),
        migrations.DeleteModel(
            name='EntryDEVSUM',
        ),
        migrations.DeleteModel(
            name='UserSettingDEV',
        ),
    ]

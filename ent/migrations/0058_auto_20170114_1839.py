# -*- coding: utf-8 -*-
# Generated by Django 1.9.7 on 2017-01-14 18:39
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('ent', '0057_auto_20170114_1737'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='possibletext',
            name='feed',
        ),
        migrations.AddField(
            model_name='possibletext',
            name='feed',
            field=models.ManyToManyField(default=1, to='ent.Feed'),
        ),
    ]

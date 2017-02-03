# -*- coding: utf-8 -*-
# Generated by Django 1.9.7 on 2017-01-14 17:37
from __future__ import unicode_literals

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('ent', '0056_auto_20170114_1721'),
    ]

    operations = [
        migrations.AddField(
            model_name='feed',
            name='description',
            field=models.CharField(default='', max_length=160),
        ),
        migrations.AlterField(
            model_name='possibletext',
            name='feed',
            field=models.ForeignKey(default=1, on_delete=django.db.models.deletion.CASCADE, to='ent.Feed'),
        ),
    ]

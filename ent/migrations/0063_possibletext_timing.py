# -*- coding: utf-8 -*-
# Generated by Django 1.9.7 on 2017-01-15 20:37
from __future__ import unicode_literals

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('ent', '0062_remove_possibletext_timing'),
    ]

    operations = [
        migrations.AddField(
            model_name='possibletext',
            name='timing',
            field=models.ForeignKey(default=1, on_delete=django.db.models.deletion.CASCADE, to='ent.Timing'),
        ),
    ]

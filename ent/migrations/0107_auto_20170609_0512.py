# -*- coding: utf-8 -*-
# Generated by Django 1.9.7 on 2017-06-09 05:12
from __future__ import unicode_literals

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('ent', '0106_auto_20170608_1707'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='possibletext',
            name='alternate',
        ),
        migrations.AddField(
            model_name='alternatetext',
            name='text',
            field=models.ForeignKey(null=True, on_delete=django.db.models.deletion.CASCADE, to='ent.PossibleText'),
        ),
    ]

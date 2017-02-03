# -*- coding: utf-8 -*-
# Generated by Django 1.9.7 on 2017-01-20 02:28
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('ent', '0075_auto_20170119_1835'),
    ]

    operations = [
        migrations.RenameModel(
            old_name='Feed',
            new_name='Collection',
        ),
        migrations.RenameField(
            model_name='collection',
            old_name='feed',
            new_name='collection',
        ),
        migrations.RenameField(
            model_name='possibletext',
            old_name='feed',
            new_name='collection',
        ),
        migrations.AlterField(
            model_name='actualtext',
            name='response',
            field=models.CharField(blank=True, max_length=160, null=True),
        ),
    ]

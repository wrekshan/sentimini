# -*- coding: utf-8 -*-
# Generated by Django 1.9.7 on 2016-10-14 22:04
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('ent', '0026_experiencesetting_unique_text_set'),
    ]

    operations = [
        migrations.AlterField(
            model_name='possibletextltm',
            name='text_type',
            field=models.CharField(default='library', max_length=120, null=True),
        ),
    ]

# -*- coding: utf-8 -*-
# Generated by Django 1.9.7 on 2017-07-05 20:02
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('ent', '0126_possibletext_creator'),
    ]

    operations = [
        migrations.AlterField(
            model_name='possibletext',
            name='text_type',
            field=models.CharField(default='consumer', max_length=160),
        ),
    ]
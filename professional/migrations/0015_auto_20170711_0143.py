# -*- coding: utf-8 -*-
# Generated by Django 1.9.7 on 2017-07-11 01:43
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('professional', '0014_group_possible_text'),
    ]

    operations = [
        migrations.AlterField(
            model_name='group',
            name='ideal_text',
            field=models.ManyToManyField(blank=True, related_name='group', to='ent.IdealText'),
        ),
    ]

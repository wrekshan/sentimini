# -*- coding: utf-8 -*-
# Generated by Django 1.9.7 on 2017-07-28 12:43
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('ent', '0138_auto_20170728_1242'),
        ('professional', '0017_person_ideal_text'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='group',
            name='collection',
        ),
        migrations.RemoveField(
            model_name='person',
            name='collection',
        ),
        migrations.AddField(
            model_name='group',
            name='program',
            field=models.ManyToManyField(blank=True, related_name='group', to='ent.Program'),
        ),
        migrations.AddField(
            model_name='person',
            name='program',
            field=models.ManyToManyField(blank=True, related_name='person', to='ent.Program'),
        ),
    ]

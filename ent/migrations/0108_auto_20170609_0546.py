# -*- coding: utf-8 -*-
# Generated by Django 1.9.7 on 2017-06-09 05:46
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('ent', '0107_auto_20170609_0512'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='alternatetext',
            name='text',
        ),
        migrations.AddField(
            model_name='possibletext',
            name='alt_text',
            field=models.ManyToManyField(blank=True, to='ent.AlternateText'),
        ),
    ]

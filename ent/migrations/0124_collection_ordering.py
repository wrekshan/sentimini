# -*- coding: utf-8 -*-
# Generated by Django 1.9.7 on 2017-06-17 17:55
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('ent', '0123_timing_text_type'),
    ]

    operations = [
        migrations.AddField(
            model_name='collection',
            name='ordering',
            field=models.CharField(default='', max_length=160),
        ),
    ]
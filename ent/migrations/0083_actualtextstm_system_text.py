# -*- coding: utf-8 -*-
# Generated by Django 1.9.7 on 2016-10-01 15:46
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('ent', '0082_actualtextltm_response_cat_bin'),
    ]

    operations = [
        migrations.AddField(
            model_name='actualtextstm',
            name='system_text',
            field=models.IntegerField(default=0),
        ),
    ]
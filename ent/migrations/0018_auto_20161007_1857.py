# -*- coding: utf-8 -*-
# Generated by Django 1.9.7 on 2016-10-07 18:57
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('ent', '0017_experiencesetting_description'),
    ]

    operations = [
        migrations.AddField(
            model_name='actualtextltm',
            name='text_set',
            field=models.CharField(default='', max_length=30, null=True),
        ),
        migrations.AddField(
            model_name='actualtextstm',
            name='text_set',
            field=models.CharField(default='', max_length=30, null=True),
        ),
        migrations.AddField(
            model_name='possibletextltm',
            name='text_set',
            field=models.CharField(default='', max_length=30, null=True),
        ),
        migrations.AddField(
            model_name='possibletextstm',
            name='text_set',
            field=models.CharField(default='', max_length=30, null=True),
        ),
    ]

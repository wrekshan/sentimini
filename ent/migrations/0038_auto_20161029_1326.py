# -*- coding: utf-8 -*-
# Generated by Django 1.9.7 on 2016-10-29 13:26
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('ent', '0037_auto_20161029_1314'),
    ]

    operations = [
        migrations.RenameField(
            model_name='feedsetting',
            old_name='ideal_id',
            new_name='feed_id',
        ),
        migrations.AddField(
            model_name='feedsetting',
            name='group_id',
            field=models.IntegerField(default=0),
        ),
        migrations.AddField(
            model_name='feedsetting',
            name='group_name',
            field=models.CharField(default='basic', max_length=120, null=True),
        ),
        migrations.AddField(
            model_name='possibletextstm',
            name='group_id',
            field=models.IntegerField(default=0),
        ),
        migrations.AddField(
            model_name='possibletextstm',
            name='group_name',
            field=models.CharField(default='basic', max_length=120, null=True),
        ),
    ]

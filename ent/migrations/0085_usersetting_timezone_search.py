# -*- coding: utf-8 -*-
# Generated by Django 1.9.7 on 2017-02-02 01:17
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('ent', '0084_collection_picture_name'),
    ]

    operations = [
        migrations.AddField(
            model_name='usersetting',
            name='timezone_search',
            field=models.CharField(default='UTC', max_length=30),
        ),
    ]

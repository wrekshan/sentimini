# -*- coding: utf-8 -*-
# Generated by Django 1.9.7 on 2017-06-15 03:03
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('ent', '0118_usersetting_text_request_stop_tmp'),
    ]

    operations = [
        migrations.AlterField(
            model_name='collection',
            name='long_description',
            field=models.TextField(default='', max_length=3000),
        ),
    ]

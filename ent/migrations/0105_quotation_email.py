# -*- coding: utf-8 -*-
# Generated by Django 1.9.7 on 2017-06-05 17:03
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('ent', '0104_auto_20170605_1656'),
    ]

    operations = [
        migrations.AddField(
            model_name='quotation',
            name='email',
            field=models.CharField(default='', max_length=5000, null=True),
        ),
    ]
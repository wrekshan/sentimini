# -*- coding: utf-8 -*-
# Generated by Django 1.9.7 on 2017-07-06 16:48
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('ent', '0131_auto_20170706_1646'),
    ]

    operations = [
        migrations.AddField(
            model_name='idealtext',
            name='edit_type',
            field=models.CharField(default='consumer', max_length=160),
        ),
    ]
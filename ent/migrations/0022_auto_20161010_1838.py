# -*- coding: utf-8 -*-
# Generated by Django 1.9.7 on 2016-10-10 18:38
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('ent', '0021_auto_20161010_1837'),
    ]

    operations = [
        migrations.AlterField(
            model_name='usersetting',
            name='active_experiences',
            field=models.CharField(default='user generated, research', max_length=5000),
        ),
    ]
# -*- coding: utf-8 -*-
# Generated by Django 1.9.7 on 2016-06-23 16:55
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('scaffold', '0002_auto_20160622_1734'),
    ]

    operations = [
        migrations.AddField(
            model_name='faquserquestions',
            name='typer',
            field=models.CharField(default='FAQ', max_length=1000, null=True),
        ),
    ]

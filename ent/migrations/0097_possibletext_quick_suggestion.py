# -*- coding: utf-8 -*-
# Generated by Django 1.9.7 on 2017-06-02 04:03
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('ent', '0096_beta_date_created'),
    ]

    operations = [
        migrations.AddField(
            model_name='possibletext',
            name='quick_suggestion',
            field=models.BooleanField(default=False),
        ),
    ]
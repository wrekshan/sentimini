# -*- coding: utf-8 -*-
# Generated by Django 1.9.7 on 2017-07-06 17:04
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('ent', '0132_idealtext_edit_type'),
    ]

    operations = [
        migrations.AlterField(
            model_name='idealtext',
            name='collection',
            field=models.ManyToManyField(blank=True, related_name='ideal_texts', to='ent.Collection'),
        ),
    ]

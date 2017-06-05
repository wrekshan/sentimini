# -*- coding: utf-8 -*-
# Generated by Django 1.9.7 on 2017-06-05 16:56
from __future__ import unicode_literals

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('ent', '0103_quotation'),
    ]

    operations = [
        migrations.AlterField(
            model_name='quotation',
            name='user',
            field=models.ForeignKey(blank=True, default=1, on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL),
        ),
    ]

# -*- coding: utf-8 -*-
# Generated by Django 1.9.7 on 2017-06-02 20:21
from __future__ import unicode_literals

import datetime
from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('ent', '0097_possibletext_quick_suggestion'),
    ]

    operations = [
        migrations.CreateModel(
            name='QuickSuggestion',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('date', models.DateTimeField(blank=True, null=True)),
                ('added', models.BooleanField(default=False)),
                ('rejected', models.BooleanField(default=False)),
                ('user', models.ForeignKey(default=1, on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL)),
            ],
        ),
        migrations.AlterField(
            model_name='timing',
            name='hour_end',
            field=models.TimeField(default=datetime.datetime(2016, 1, 30, 21, 0)),
        ),
        migrations.AlterField(
            model_name='timing',
            name='hour_start',
            field=models.TimeField(default=datetime.datetime(2016, 1, 30, 9, 0)),
        ),
    ]

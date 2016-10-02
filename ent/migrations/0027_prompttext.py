# -*- coding: utf-8 -*-
# Generated by Django 1.9.7 on 2016-08-09 17:38
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('ent', '0026_emotionontology_prompt_set_percent_calc'),
    ]

    operations = [
        migrations.CreateModel(
            name='Prompttext',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('text', models.CharField(default='How much XXX is in your present moment (0-10)?', max_length=500, null=True)),
                ('text_type', models.CharField(default='DIM', max_length=500, null=True)),
                ('text_percent', models.IntegerField(default=10)),
            ],
        ),
    ]

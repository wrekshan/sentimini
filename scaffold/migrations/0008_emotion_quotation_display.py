# -*- coding: utf-8 -*-
# Generated by Django 1.9.7 on 2016-07-19 18:47
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('scaffold', '0007_auto_20160716_0549'),
    ]

    operations = [
        migrations.CreateModel(
            name='emotion_quotation_display',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('emotion', models.CharField(default='', max_length=1000, null=True)),
                ('emotion_id', models.IntegerField(default=0)),
                ('quotation', models.TextField(default='QUOTATION: EMOTIONS MAKE UP OUR WORLD', null=True)),
                ('author', models.CharField(default='AUTHOR', max_length=3000, null=True)),
            ],
        ),
    ]

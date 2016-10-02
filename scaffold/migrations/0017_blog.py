# -*- coding: utf-8 -*-
# Generated by Django 1.9.7 on 2016-09-16 17:12
from __future__ import unicode_literals

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('scaffold', '0016_auto_20160901_2254'),
    ]

    operations = [
        migrations.CreateModel(
            name='Blog',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('author', models.CharField(default='William Rekshan', max_length=1000)),
                ('title', models.CharField(default='', max_length=1000, null=True)),
                ('content', models.TextField(default='Default Content Here', max_length=1000)),
                ('user', models.ForeignKey(default=1, on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL)),
            ],
        ),
    ]

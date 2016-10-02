# -*- coding: utf-8 -*-
# Generated by Django 1.9.7 on 2016-07-17 17:29
from __future__ import unicode_literals

from decimal import Decimal
from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('vis', '0006_auto_20160716_1757'),
    ]

    operations = [
        migrations.CreateModel(
            name='EntryDEVSUM',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('test_user', models.CharField(default='', max_length=160, null=True)),
                ('prompt', models.CharField(default='', max_length=160, null=True)),
                ('prompt_type', models.CharField(default='', max_length=160, null=True)),
                ('prompt_reply', models.IntegerField(default=0)),
                ('prompt_reply_avg', models.DecimalField(decimal_places=2, default=Decimal('0.0'), max_digits=3)),
                ('prompt_reply_count', models.IntegerField(default=0)),
                ('user', models.ForeignKey(default=1, on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL)),
            ],
        ),
    ]
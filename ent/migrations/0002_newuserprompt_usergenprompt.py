# -*- coding: utf-8 -*-
# Generated by Django 1.9.7 on 2016-06-16 19:27
from __future__ import unicode_literals

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('ent', '0001_initial'),
    ]

    operations = [
        migrations.CreateModel(
            name='NewUserPrompt',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('prompt', models.CharField(default='', max_length=160, null=True)),
                ('prompt_type', models.CharField(default='', max_length=120, null=True)),
                ('NUP_seq', models.IntegerField(default=0)),
                ('send_next_immediately', models.BooleanField(default=False)),
            ],
        ),
        migrations.CreateModel(
            name='UserGenPrompt',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('prompt', models.CharField(default='', max_length=160, null=True)),
                ('date_created', models.DateTimeField(blank=True, null=True)),
                ('active', models.BooleanField(default=True)),
                ('show_user', models.BooleanField(default=True)),
                ('user', models.ForeignKey(default=1, on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL)),
            ],
        ),
    ]
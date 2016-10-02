# -*- coding: utf-8 -*-
# Generated by Django 1.9.7 on 2016-08-03 04:33
from __future__ import unicode_literals

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('scaffold', '0012_betasurvey'),
    ]

    operations = [
        migrations.CreateModel(
            name='emotion_statement_display',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('emotion', models.CharField(default='', max_length=1000, null=True)),
                ('emotion_id', models.IntegerField(default=0)),
                ('statement_type', models.CharField(default='', max_length=1000)),
                ('show_me', models.IntegerField(default=0)),
                ('number_of_likes', models.IntegerField(default=0)),
                ('quotation', models.CharField(default='QUOTATION: EMOTIONS MAKE UP OUR WORLD', max_length=3000, null=True)),
                ('author', models.CharField(default='AUTHOR', max_length=3000, null=True)),
            ],
        ),
        migrations.CreateModel(
            name='user_likes',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('statement_id', models.IntegerField(default=0)),
                ('user', models.ForeignKey(default=1, on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL)),
            ],
        ),
        migrations.DeleteModel(
            name='emotion_instruction_display',
        ),
        migrations.DeleteModel(
            name='emotion_quotation_display',
        ),
    ]

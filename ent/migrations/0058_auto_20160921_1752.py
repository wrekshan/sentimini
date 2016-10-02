# -*- coding: utf-8 -*-
# Generated by Django 1.9.7 on 2016-09-21 17:52
from __future__ import unicode_literals

from django.conf import settings
import django.core.validators
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('ent', '0057_auto_20160919_1815'),
    ]

    operations = [
        migrations.CreateModel(
            name='ActualTextLTM',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('text_id', models.IntegerField(default=0)),
                ('textstore_id', models.IntegerField(default=0)),
                ('text', models.CharField(default='', max_length=160, null=True)),
                ('text_type', models.CharField(default='user', max_length=120, null=True)),
                ('response', models.CharField(default='', max_length=160, null=True)),
                ('response_cat', models.CharField(default='', max_length=160, null=True)),
                ('response_dim', models.IntegerField(blank=True, null=True)),
                ('time_response', models.DateTimeField(blank=True, null=True)),
                ('time_to_send', models.DateTimeField(blank=True, null=True)),
                ('time_sent', models.DateTimeField(blank=True, null=True)),
                ('simulated', models.IntegerField(default=0)),
                ('user', models.ForeignKey(default=1, on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL)),
            ],
        ),
        migrations.CreateModel(
            name='ActualTextSTM',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('text_id', models.IntegerField(default=0)),
                ('textstore_id', models.IntegerField(default=0)),
                ('text', models.CharField(default='', max_length=160, null=True)),
                ('text_type', models.CharField(default='user', max_length=120, null=True)),
                ('time_to_send', models.DateTimeField(blank=True, null=True)),
                ('time_sent', models.DateTimeField(blank=True, null=True)),
                ('simulated', models.IntegerField(default=0)),
                ('user', models.ForeignKey(default=1, on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL)),
            ],
        ),
        migrations.CreateModel(
            name='PossibleTextLTM',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('text', models.CharField(default='', max_length=160, null=True)),
                ('text_type', models.CharField(default='user', max_length=120, null=True)),
                ('text_importance', models.IntegerField(default=0, validators=[django.core.validators.MinValueValidator(0), django.core.validators.MaxValueValidator(100)])),
                ('response_type', models.CharField(default='Open', max_length=100)),
                ('show_user', models.BooleanField(default=False)),
                ('date_created', models.DateTimeField(blank=True, null=True)),
                ('date_altered', models.DateTimeField(blank=True, null=True)),
                ('user', models.ForeignKey(default=1, on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL)),
            ],
        ),
        migrations.CreateModel(
            name='PossibleTextSTM',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('text', models.CharField(default='', max_length=160, null=True)),
                ('text_type', models.CharField(default='user', max_length=120, null=True)),
                ('text_importance', models.IntegerField(default=0, validators=[django.core.validators.MinValueValidator(0), django.core.validators.MaxValueValidator(100)])),
                ('response_type', models.CharField(default='Open', max_length=100)),
                ('show_user', models.BooleanField(default=False)),
                ('date_created', models.DateTimeField(blank=True, null=True)),
                ('date_altered', models.DateTimeField(blank=True, null=True)),
                ('user', models.ForeignKey(default=1, on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL)),
            ],
        ),
        migrations.RemoveField(
            model_name='emotion',
            name='user',
        ),
        migrations.RemoveField(
            model_name='entry',
            name='user',
        ),
        migrations.DeleteModel(
            name='NewUserPrompt',
        ),
        migrations.RemoveField(
            model_name='usergenprompt',
            name='user',
        ),
        migrations.RemoveField(
            model_name='usergenpromptstore',
            name='user',
        ),
        migrations.RemoveField(
            model_name='usersummary',
            name='user',
        ),
        migrations.DeleteModel(
            name='Emotion',
        ),
        migrations.DeleteModel(
            name='Entry',
        ),
        migrations.DeleteModel(
            name='UserGenPrompt',
        ),
        migrations.DeleteModel(
            name='UserGenPromptStore',
        ),
        migrations.DeleteModel(
            name='UserSummary',
        ),
    ]

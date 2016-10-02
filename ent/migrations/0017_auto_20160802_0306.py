# -*- coding: utf-8 -*-
# Generated by Django 1.9.7 on 2016-08-02 03:06
from __future__ import unicode_literals

from django.conf import settings
import django.core.validators
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('ent', '0016_entry_response_time'),
    ]

    operations = [
        migrations.CreateModel(
            name='EmotionOntology',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('ontological_name', models.CharField(default='default', max_length=300)),
                ('prompt_set', models.CharField(default='default', max_length=300)),
                ('prompt_set_percent', models.IntegerField(default=0, validators=[django.core.validators.MinValueValidator(0), django.core.validators.MaxValueValidator(100)])),
                ('user', models.ForeignKey(default=1, on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL)),
            ],
        ),
        migrations.RenameField(
            model_name='emotion',
            old_name='emotion_type',
            new_name='prompt_set',
        ),
        migrations.AddField(
            model_name='emotion',
            name='prompt_percent',
            field=models.IntegerField(default=0, validators=[django.core.validators.MinValueValidator(0), django.core.validators.MaxValueValidator(100)]),
        ),
        migrations.AddField(
            model_name='usersetting',
            name='emotion_ontology_current',
            field=models.CharField(default='default', max_length=300),
        ),
        migrations.AddField(
            model_name='usersetting',
            name='global_settings_current',
            field=models.CharField(default='default', max_length=300),
        ),
        migrations.AddField(
            model_name='usersetting',
            name='user_settings_current',
            field=models.CharField(default='default', max_length=300),
        ),
    ]

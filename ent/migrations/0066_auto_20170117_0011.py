# -*- coding: utf-8 -*-
# Generated by Django 1.9.7 on 2017-01-17 00:11
from __future__ import unicode_literals

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('ent', '0065_auto_20170115_2109'),
    ]

    operations = [
        migrations.CreateModel(
            name='Tag',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('tag', models.CharField(blank=True, max_length=160, null=True)),
                ('user', models.ForeignKey(default=1, on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL)),
            ],
        ),
        migrations.AddField(
            model_name='feed',
            name='tag',
            field=models.ManyToManyField(blank=True, null=True, to='ent.Tag'),
        ),
        migrations.AddField(
            model_name='possibletext',
            name='tag',
            field=models.ManyToManyField(blank=True, null=True, to='ent.Tag'),
        ),
    ]

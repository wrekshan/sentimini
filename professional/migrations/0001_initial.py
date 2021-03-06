# -*- coding: utf-8 -*-
# Generated by Django 1.9.7 on 2017-07-03 17:16
from __future__ import unicode_literals

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('ent', '0125_usersetting_location'),
    ]

    operations = [
        migrations.CreateModel(
            name='group',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('group', models.CharField(default='', max_length=1000, null=True)),
                ('creator', models.ForeignKey(default=1, on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL)),
            ],
        ),
        migrations.CreateModel(
            name='Person',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('creator', models.ForeignKey(default=1, on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL)),
                ('person', models.ForeignKey(default=1, on_delete=django.db.models.deletion.CASCADE, to='ent.UserSetting')),
            ],
        ),
        migrations.AddField(
            model_name='group',
            name='person',
            field=models.ManyToManyField(blank=True, to='professional.Person'),
        ),
    ]

# -*- coding: utf-8 -*-
# Generated by Django 1.9.7 on 2016-08-13 19:26
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('ent', '0030_entry_prompt_reply_type'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='usergenprompt',
            name='require_response',
        ),
        migrations.AddField(
            model_name='usergenprompt',
            name='response_type',
            field=models.CharField(default='Open', max_length=100),
        ),
    ]
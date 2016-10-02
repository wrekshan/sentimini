# -*- coding: utf-8 -*-
# Generated by Django 1.9.7 on 2016-10-02 02:32
from __future__ import unicode_literals

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.CreateModel(
            name='BETAsurvey',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('answered', models.IntegerField(default=0)),
                ('how_many_prompts', models.IntegerField(default=0)),
                ('text_topics', models.CharField(default='', max_length=1000, null=True)),
                ('desired_dollars', models.IntegerField(default=0)),
                ('max_dollars', models.IntegerField(default=0)),
                ('new_features', models.CharField(default='', max_length=1000, null=True)),
                ('new_directions', models.CharField(default='', max_length=1000, null=True)),
                ('user', models.ForeignKey(default=1, on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL)),
            ],
        ),
        migrations.CreateModel(
            name='Blog',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('author', models.CharField(default='William Rekshan', max_length=1000)),
                ('title', models.CharField(default='', max_length=1000, null=True)),
                ('description', models.TextField(default='Default Description', max_length=10000)),
                ('content', models.TextField(default='Default Content Here', max_length=100000)),
                ('date_created', models.DateTimeField(blank=True, null=True)),
                ('date_altered', models.DateTimeField(blank=True, null=True)),
                ('user', models.ForeignKey(default=1, on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL)),
            ],
        ),
        migrations.CreateModel(
            name='Business',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(default='Business Set 1', max_length=300)),
                ('con_price_per_outgoing', models.DecimalField(decimal_places=5, default=0.0035, max_digits=5)),
                ('con_price_per_inccming', models.DecimalField(decimal_places=5, default=0.0, max_digits=5)),
                ('con_number_outgoing_per_free_per_day', models.IntegerField(default=2)),
                ('con_number_ingoing_per_free_per_day', models.IntegerField(default=1)),
                ('con_number_outgoing_per_paid_per_day', models.IntegerField(default=10)),
                ('con_number_ingoing_per_paid_per_day', models.IntegerField(default=6)),
                ('con_conversation_rate_to_paid', models.DecimalField(decimal_places=3, default=0.01, max_digits=3)),
                ('con_return_per_paying_user_per_month', models.IntegerField(default=10)),
                ('static_human_cost_per_month', models.IntegerField(default=5800)),
                ('static_server_cost_per_month', models.IntegerField(default=150)),
                ('static_other_cost_per_month', models.IntegerField(default=150)),
                ('user', models.ForeignKey(default=1, on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL)),
            ],
        ),
        migrations.CreateModel(
            name='emotion_instruction',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('email', models.CharField(default='', max_length=1000, null=True)),
                ('emotion', models.CharField(default='', max_length=1000, null=True)),
                ('quotation', models.TextField(default='', max_length=3000, null=True)),
                ('why', models.CharField(default='', max_length=3000, null=True)),
            ],
        ),
        migrations.CreateModel(
            name='emotion_quotation',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('email', models.CharField(default='', max_length=1000, null=True)),
                ('emotion', models.CharField(default='', max_length=1000, null=True)),
                ('quotation', models.TextField(default='', max_length=3000, null=True)),
                ('author', models.CharField(default='', max_length=3000, null=True)),
            ],
        ),
        migrations.CreateModel(
            name='emotion_statement_display',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('emotion', models.CharField(default='', max_length=1000, null=True)),
                ('emotion_id', models.IntegerField(default=0)),
                ('statement_type', models.CharField(default='', max_length=1000)),
                ('show_me', models.IntegerField(default=0)),
                ('number_of_likes', models.IntegerField(default=0)),
                ('statement', models.TextField(default='QUOTATION: EMOTIONS MAKE UP OUR WORLD', max_length=3000, null=True)),
                ('author', models.CharField(default='AUTHOR', max_length=3000, null=True)),
            ],
        ),
        migrations.CreateModel(
            name='FAQ',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('question', models.CharField(default='', max_length=1000, null=True)),
                ('answer', models.TextField(default='')),
                ('category', models.CharField(default='', max_length=1000, null=True)),
                ('date_created', models.DateTimeField(auto_now_add=True)),
                ('date_updated', models.DateTimeField(auto_now=True)),
                ('active', models.BooleanField(default=True)),
            ],
        ),
        migrations.CreateModel(
            name='FAQuserquestions',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('typer', models.CharField(default='FAQ', max_length=1000, null=True)),
                ('question', models.CharField(default='', max_length=1000, null=True)),
                ('date_created', models.DateTimeField(auto_now_add=True)),
                ('user', models.ForeignKey(default=1, on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL)),
            ],
        ),
        migrations.CreateModel(
            name='Measure',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(default='Set Name', max_length=300)),
                ('measure', models.CharField(default='Measure Name', max_length=300)),
                ('super_measure', models.CharField(default='Super Measure', max_length=300)),
                ('measure_type', models.CharField(default='Dimensional', max_length=300)),
                ('population', models.CharField(default='Group', max_length=300)),
                ('minval', models.IntegerField(default=0)),
                ('maxval', models.IntegerField(default=10)),
                ('mean', models.IntegerField(default=5)),
                ('sd', models.IntegerField(default=3)),
                ('distr', models.CharField(default='Normal', max_length=300)),
                ('response_rate', models.IntegerField(default=60)),
                ('user', models.ForeignKey(default=1, on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL)),
            ],
        ),
        migrations.CreateModel(
            name='Sentimini_help',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('help_heading', models.CharField(default='Text', max_length=300)),
                ('help_content', models.TextField(default='Default content', max_length=10000)),
                ('help_type', models.CharField(default='Glossary', max_length=300)),
                ('major_cat', models.CharField(default='Settings', max_length=300)),
                ('minor_cat', models.CharField(default='Texts', max_length=300)),
                ('level', models.CharField(blank=True, default='', max_length=300, null=True)),
                ('user', models.ForeignKey(default=1, on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL)),
            ],
        ),
        migrations.CreateModel(
            name='user_likes',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('statement_id', models.IntegerField(default=0)),
                ('like_switch', models.IntegerField(default=0)),
                ('user', models.ForeignKey(default=1, on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL)),
            ],
        ),
    ]

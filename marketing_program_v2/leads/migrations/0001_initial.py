# -*- coding: utf-8 -*-

from __future__ import unicode_literals

import django.contrib.postgres.fields.jsonb
from django.db import migrations, models
import django.db.models.manager


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Fields',
            fields=[
                ('id', models.IntegerField(primary_key=True, serialize=False, verbose_name='id')),
                ('display_name', models.CharField(max_length=255, verbose_name='display_name')),
                ('data_type', models.CharField(max_length=255, verbose_name='data_type')),
                ('length', models.IntegerField(null=True, verbose_name='length')),
                ('rest_name', models.CharField(blank=True, max_length=255, verbose_name='rest_name')),
                ('rest_read_only', models.NullBooleanField(verbose_name='rest_read_only')),
                ('soap_name', models.CharField(blank=True, max_length=255, verbose_name='soapName')),
                ('soap_read_only', models.NullBooleanField(verbose_name='soap_read_only')),
            ],
            options={
                'db_table': 'fields',
            },
            managers=[
                ('object', django.db.models.manager.Manager()),
            ],
        ),
        migrations.CreateModel(
            name='Leads',
            fields=[
                ('id', models.IntegerField(primary_key=True, serialize=False, verbose_name='id')),
                ('email', models.CharField(max_length=255, null=True, verbose_name='email')),
                ('updated_at', models.DateTimeField(null=True, verbose_name='updated_at')),
                ('created_at', models.DateTimeField(null=True, verbose_name='created_at')),
                ('last_name', models.CharField(max_length=255, null=True, verbose_name='last_name')),
                ('first_name', models.CharField(max_length=255, null=True, verbose_name='first_name')),
                ('document', django.contrib.postgres.fields.jsonb.JSONField(null=True, verbose_name='document')),
            ],
            options={
                'db_table': 'leads',
            },
            managers=[
                ('object', django.db.models.manager.Manager()),
            ],
        ),
    ]

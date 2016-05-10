# -*- coding: utf-8 -*-
# Generated by Django 1.9.4 on 2016-05-10 04:34
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('users', '0002_auto_20160509_2129'),
    ]

    operations = [
        migrations.AddField(
            model_name='user',
            name='client_id',
            field=models.CharField(blank=True, max_length=255, verbose_name='Client ID'),
        ),
        migrations.AddField(
            model_name='user',
            name='client_secret',
            field=models.CharField(blank=True, max_length=255, verbose_name='Client Secret'),
        ),
    ]

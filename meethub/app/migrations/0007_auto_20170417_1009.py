# -*- coding: utf-8 -*-
# Generated by Django 1.10.6 on 2017-04-17 10:09
from __future__ import unicode_literals

import datetime
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('app', '0006_auto_20170417_0851'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='activity',
            name='date',
        ),
        migrations.RemoveField(
            model_name='activity',
            name='time',
        ),
        migrations.AddField(
            model_name='activity',
            name='date_time',
            field=models.DateTimeField(null=True),
        ),
        migrations.AlterField(
            model_name='invitation',
            name='create_at',
            field=models.DateTimeField(default=datetime.datetime(2017, 4, 17, 10, 9, 55, 542784)),
        ),
    ]

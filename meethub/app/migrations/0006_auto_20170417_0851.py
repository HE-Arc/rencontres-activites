# -*- coding: utf-8 -*-
# Generated by Django 1.10.6 on 2017-04-17 08:51
from __future__ import unicode_literals

import datetime
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('app', '0005_invitation'),
    ]

    operations = [
        migrations.AlterField(
            model_name='invitation',
            name='create_at',
            field=models.DateTimeField(default=datetime.datetime(2017, 4, 17, 8, 51, 38, 437373)),
        ),
    ]

# -*- coding: utf-8 -*-
# Generated by Django 1.11.15 on 2019-04-12 01:23
from __future__ import unicode_literals

import datetime
from django.db import migrations, models
from django.utils.timezone import utc


class Migration(migrations.Migration):

    dependencies = [
        ('article', '0010_auto_20190411_1731'),
    ]

    operations = [
        migrations.AlterField(
            model_name='articlepost',
            name='created',
            field=models.DateTimeField(default=datetime.datetime(2019, 4, 12, 1, 23, 58, 697835, tzinfo=utc)),
        ),
    ]

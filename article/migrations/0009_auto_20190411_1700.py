# -*- coding: utf-8 -*-
# Generated by Django 1.11.15 on 2019-04-11 09:00
from __future__ import unicode_literals

import datetime
from django.db import migrations, models
from django.utils.timezone import utc


class Migration(migrations.Migration):

    dependencies = [
        ('article', '0008_auto_20190411_1431'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='articlepost',
            name='avatar',
        ),
        migrations.AlterField(
            model_name='articlepost',
            name='created',
            field=models.DateTimeField(default=datetime.datetime(2019, 4, 11, 9, 0, 23, 519503, tzinfo=utc)),
        ),
    ]

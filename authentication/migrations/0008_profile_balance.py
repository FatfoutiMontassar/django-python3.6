# -*- coding: utf-8 -*-
# Generated by Django 1.10.4 on 2017-10-09 20:24
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('authentication', '0007_activity_table'),
    ]

    operations = [
        migrations.AddField(
            model_name='profile',
            name='balance',
            field=models.IntegerField(default=0, null=True),
        ),
    ]

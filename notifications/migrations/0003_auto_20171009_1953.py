# -*- coding: utf-8 -*-
# Generated by Django 1.10.4 on 2017-10-09 19:53
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('notifications', '0002_notification_product'),
    ]

    operations = [
        migrations.AlterField(
            model_name='notification',
            name='notification_type',
            field=models.CharField(choices=[('normal', 'normal'), ('smile', 'smile'), ('love', 'love'), ('wish', 'wish'), ('like', 'like'), ('dislike', 'dislike')], max_length=1),
        ),
    ]

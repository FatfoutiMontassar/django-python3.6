# -*- coding: utf-8 -*-
# Generated by Django 1.10 on 2017-06-30 09:31
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('shop', '0024_auto_20170630_1008'),
    ]

    operations = [
        migrations.AddField(
            model_name='product',
            name='Ptype',
            field=models.IntegerField(choices=[(1, 'Tous les articles'), (2, 'Faits main'), (3, 'Vintage')], default=1, null=True),
        ),
    ]

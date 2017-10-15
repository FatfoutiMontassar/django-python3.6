# -*- coding: utf-8 -*-
# Generated by Django 1.11.3 on 2017-10-15 13:24
from __future__ import unicode_literals

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('collection', '0001_initial'),
        ('shop', '0043_product_ccategorie'),
        ('promote', '0001_initial'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='promote',
            name='collections',
        ),
        migrations.AddField(
            model_name='promote',
            name='collections',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, related_name='promote_collections', to='collection.Collection'),
        ),
        migrations.RemoveField(
            model_name='promote',
            name='products',
        ),
        migrations.AddField(
            model_name='promote',
            name='products',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, related_name='promote_products', to='shop.Product'),
        ),
    ]
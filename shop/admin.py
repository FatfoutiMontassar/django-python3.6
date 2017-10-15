# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.contrib import admin

from .models import Product , Table , Contact , Trader , albumImage

# Register your models here.

admin.site.register(Product)
admin.site.register(Table)
admin.site.register(Contact)
admin.site.register(Trader)
admin.site.register(albumImage)

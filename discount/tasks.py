from __future__ import absolute_import, unicode_literals
import random
from celery.decorators import task
from discount.models import Discount
from django.shortcuts import get_object_or_404

@task(name="sum_two_numbers")
def add(x, y):
    return x + y

@task(name="multiply_two_numbers")
def mul(x, y):
    total = x * (y * random.randint(3, 100))
    return total

@task(name="sum_list_numbers")
def xsum(numbers):
    return sum(numbers)

@task(name="activate")
def activate(discount_id):
    discount = get_object_or_404(Discount,id=discount_id)
    discount.isActive = (not discount.isActive) 
    discount.save()
    print ("success..")
    return True

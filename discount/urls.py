from django.conf.urls import url , include

from django.contrib import admin

from django.conf import settings

from django.conf.urls.static import static

from . import views

urlpatterns = [
    url(r'^$',views.discounts , name='discounts'),
	url(r'^new',views.newDiscount , name='newDiscount'),
    url(r'^mine',views.myDiscounts , name='myDiscounts'),
]

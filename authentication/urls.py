from django.conf.urls import url , include

from django.contrib import admin

from django.conf import settings

from django.conf.urls.static import static

from . import views

urlpatterns = [
    url(r'^register',views.register , name='register'),
	url(r'^login',views.login , name='login'),
	url(r'^logout',views.logout , name='logout'),
]

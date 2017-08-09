from django.conf.urls import url , include

from django.contrib import admin

from django.conf import settings

from django.conf.urls.static import static

from . import views

urlpatterns = [
    url(r'^$', views.notifications,name='notifications_all'),
    url(r'^check/$', views.notifications_check , name='notifications_check' ),
    url(r'^last/$', views.notifications_last , name='notifications_last' ),
]

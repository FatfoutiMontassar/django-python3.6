from django.conf.urls import url , include

from django.contrib import admin

from django.conf import settings

from django.conf.urls.static import static

from . import views

urlpatterns = [
    url(r'^reactionRemove/(?P<id>\w{0,50})/$', views.reactionRemove , name='reactionRemove' ),
	url(r'^reactionLike/(?P<id>\w{0,50})/$', views.reactionLike , name='reactionLike' ),
	url(r'^reactionLove/(?P<id>\w{0,50})/$', views.reactionLove , name='reactionLove' ),
	url(r'^reactionWow/(?P<id>\w{0,50})/$', views.reactionWow , name='reactionWow' ),
]

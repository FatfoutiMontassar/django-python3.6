from django.conf.urls import url , include

from django.contrib import admin

from django.conf import settings

from django.conf.urls.static import static

from . import views

urlpatterns = [
    url(r'^reactionRemove/(?P<id>\w{0,50})/$', views.reactionRemove , name='reactionRemove' ),
	url(r'^reactionNormal/(?P<id>\w{0,50})/$', views.reactionNormal , name='reactionNormal' ),
	url(r'^reactionSmile/(?P<id>\w{0,50})/$', views.reactionSmile , name='reactionSmile' ),
	url(r'^reactionLove/(?P<id>\w{0,50})/$', views.reactionLove , name='reactionLove' ),
	url(r'^reactionWish/(?P<id>\w{0,50})/$', views.reactionWish , name='reactionWish' ),
]

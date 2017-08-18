from django.conf.urls import url , include

from django.contrib import admin

from django.conf import settings

from django.conf.urls.static import static

from . import views

urlpatterns = [
    url(r'^$', views.collection_all , name='collection_all' ),
    url(r'^newCollection/$', views.newCollection , name='newCollection' ),
    url(r'^mine/$', views.mineCollections , name='mineCollection' ),
    url(r'^deleteCollection/(?P<id>\w{0,50})/$', views.deleteCollection , name='deleteCollection' ),
    url(r'^view/(?P<id>\w{0,50})/$', views.viewCollections , name='viewCollection' ),
    url(r'^edit/(?P<id>\w{0,50})/$', views.editCollections , name='editCollection' ),
]

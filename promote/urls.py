from django.conf.urls import url , include

from django.contrib import admin

from django.conf import settings

from django.conf.urls.static import static

from . import views

urlpatterns = [
	url(r'^$', views.all , name='allPromotes' ),
	url(r'^redirectSettings/$', views.settings , name='redirect_settings' ),
	url(r'^redirectInfo/$', views.info , name='redirect_info' ),
	url(r'^redirectPayment/$', views.payment , name='redirect_payment' ),
	url(r'^redirectAbout/$', views.about , name='redirect_about' ),
	url(r'^redirectOptions/$', views.options , name='redirect_options' ),
	url(r'^redirectPromote/$', views.promote , name='redirect_promote' ),
	url(r'^redirectListings/$', views.listings , name='redirect_listings' ),
]

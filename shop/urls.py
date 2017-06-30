from django.conf.urls import url , include

from django.contrib import admin

from django.conf import settings

from django.conf.urls.static import static

from . import views

urlpatterns = [
	url(r'^$', views.discover , name='discover' ),
	url(r'^discover/$', views.discover , name='discover' ),
	url(r'^discovermore/(?P<id>\w{0,50})/$', views.discovermore , name='discovermore' ),
	url(r'^discovermore/(?P<idC>\w{0,50})/(?P<idP>\w{0,50})/$', views.categories , name='categories' ),
	url(r'^stores',views.storesView , name='stores'),
	url(r'^details/(?P<id>\w{0,50})/$',views.details),
	url(r'^deleteStore/(?P<id>\w{0,50})/$',views.deleteStore),
	url(r'^deleteProduct/(?P<id>\w{0,50})/$',views.deleteProduct),
	#url(r'^product/(?P<id>\w{0,50})/$',views.product),
	#url(r'^add',views.add , name='add'),
	url(r'^addProduct/(?P<id>\w{0,50})/$',views.addProduct,name='addProduct'),
	url(r'^product_create/(?P<id>\w{0,50})/$',views.product_create,name='product_create'),
	url(r'^store_details/(?P<id>\w{0,50})/$',views.store_details , name='store_details'),
	url(r'^newStore',views.newStore, name='newStore'),
	url(r'^store_create',views.store_create , name='store_create'),
	url(r'^logout',views.logout , name='logout'),
	url(r'^contact_create',views.contact_create , name='contact_create'),
	url(r'^product_details/(?P<id>\w{0,50})/$', views.product_details , name='product_details'),
	url(r'^register',views.register , name='register'),
	url(r'^login',views.login , name='login'),
]

'''
if settings.DEBUG:
	urlpatterns += static(settings.STATIC_URL,document_root=settings.STATIC_ROOT)
	urlpatterns += static(settings.MEDIA_URL,document_root=settings.MEDIA_ROOT)
'''

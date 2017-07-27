from django.conf.urls import url , include

from django.contrib import admin

from django.conf import settings

from django.conf.urls.static import static

from . import views

urlpatterns = [
	url(r'^$', views.discover , name='discover' ),
	url(r'^discover/$', views.discover , name='discover' ),
	url(r'^products/$', views.products , name='products' ),
	url(r'^discover/(?P<idP>\w{0,50})/$', views.discover , name='discover' ),

	url(r'^reactionRemove/(?P<id>\w{0,50})/$', views.reactionRemove , name='reactionRemove' ),
	url(r'^reactionLike/(?P<id>\w{0,50})/$', views.reactionLike , name='reactionLike' ),
	url(r'^reactionLove/(?P<id>\w{0,50})/$', views.reactionLove , name='reactionLove' ),
	url(r'^reactionWow/(?P<id>\w{0,50})/$', views.reactionWow , name='reactionWow' ),

	url(r'^likeProduct/(?P<id>\w{0,50})/$', views.likeProduct , name='likeProduct' ),
	url(r'^smileProduct/(?P<id>\w{0,50})/$', views.smileProduct , name='smileProduct' ),
	url(r'^wishProduct/(?P<id>\w{0,50})/$', views.wishProduct , name='wishProduct' ),
	url(r'^discover/(?P<idC>\w{0,50})/(?P<idP>\w{0,50})/$', views.discover , name='discover' ),
	url(r'^discover/(?P<idC>\w{0,50})/(?P<idP>\w{0,50})/(?P<Ptype>[\w\-]+)/$', views.discover , name='discover' ),
	url(r'^search/$', views.search , name='search' ),
	url(r'^stores',views.storesView , name='stores'),
	url(r'^details/(?P<id>\w{0,50})/$',views.details),
	url(r'^details/(?P<id>\w{0,50})/page=(?P<idP>\w{0,50})/$',views.details),
	url(r'^album/(?P<id>\w{0,50})/$',views.album),
	url(r'^activateProduct/(?P<id>\w{0,50})/$',views.activateProduct),
	url(r'^addStoreImage/(?P<id>\w{0,50})/$',views.addStoreImage,name="addStoreImage"),
	url(r'^addProductMainImage/(?P<id>\w{0,50})/$',views.addProductMainImage,name="addProductMainImage"),
	url(r'^duplicateProduct/(?P<id>\w{0,50})/$',views.duplicateProduct,name="duplicateProduct"),
	url(r'^deleteStore/(?P<id>\w{0,50})/$',views.deleteStore),
	url(r'^deleteProduct/(?P<id>\w{0,50})/$',views.deleteProduct),
	url(r'^editProduct/(?P<id>\w{0,50})/$',views.editProduct,name="editProduct"),
	url(r'^editStore/(?P<id>\w{0,50})/$',views.editStore,name="editStore"),
	url(r'^editProduct/(?P<id>\w{0,50})/$',views.editProduct,name="editProduct"),
	url(r'^addProduct/(?P<id>\w{0,50})/$',views.addProduct,name='addProduct'),
	url(r'^product_create/(?P<id>\w{0,50})/$',views.product_create,name='product_create'),
	url(r'^store_details/(?P<id>\w{0,50})/$',views.store_details , name='store_details'),
	url(r'^newStore',views.newStore, name='newStore'),
	url(r'^store_create/(?P<comment>[\w\-]+)/$',views.store_create , name='store_create'),
	url(r'^logout',views.logout , name='logout'),
	url(r'^contact_create',views.contact_create , name='contact_create'),
	url(r'^product_details/(?P<id>\w{0,50})/$', views.product_details , name='product_details'),
	url(r'^register',views.register , name='register'),
	url(r'^login',views.login , name='login'),
]

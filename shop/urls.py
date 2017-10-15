from django.conf.urls import url , include

from django.contrib import admin

from django.conf import settings

from django.conf.urls.static import static

from . import views

urlpatterns = [

	url(r'^products/$', views.products , name='products' ),
	url(r'^tables/$',views.tablesView , name='tables'),
	url(r'^wishlist',views.wishlist , name='wishlist'),
	url(r'^details/(?P<id>\w{0,50})/$',views.details),
	url(r'^view/(?P<id>\w{0,50})/$',views.view),
	url(r'^view/(?P<id>\w{0,50})/(?P<idP>\w{0,50})/$',views.view),
	url(r'^tablesAlbum/(?P<id>\w{0,50})/$',views.tablesAlbum),
	url(r'^details/(?P<id>\w{0,50})/page=(?P<idP>\w{0,50})/$',views.details),
	url(r'^album/(?P<id>\w{0,50})/$',views.album),
	url(r'^activateProduct/(?P<id>\w{0,50})/$',views.activateProduct),
	url(r'^addTableImage/(?P<id>\w{0,50})/$',views.addTableImage,name="addTableImage"),
	url(r'^addProductMainImage/(?P<id>\w{0,50})/$',views.addProductMainImage,name="addProductMainImage"),
	url(r'^duplicateProduct/(?P<id>\w{0,50})/$',views.duplicateProduct,name="duplicateProduct"),
	url(r'^deleteTable/(?P<id>\w{0,50})/$',views.deleteTable),
	url(r'^deleteProduct/(?P<id>\w{0,50})/$',views.deleteProduct),
	url(r'^editProduct/(?P<id>\w{0,50})/$',views.editProduct,name="editProduct"),
	url(r'^editTable/(?P<id>\w{0,50})/$',views.editTable,name="editTable"),
	url(r'^editProduct/(?P<id>\w{0,50})/$',views.editProduct,name="editProduct"),
	url(r'^addProduct/(?P<id>\w{0,50})/$',views.addProduct,name='addProduct'),
	url(r'^product_create/(?P<id>\w{0,50})/$',views.product_create,name='product_create'),
	url(r'^newTable',views.newTable, name='newTable'),
	url(r'^table_create/(?P<comment>[\w\-]+)/$',views.table_create , name='table_create'),
	url(r'^table_details/(?P<id>\w{0,50})/$',views.table_details , name='table_details'),

	url(r'^contact_create',views.contact_create , name='contact_create'),
	url(r'^product_details/(?P<id>\w{0,50})/$', views.product_details , name='product_details'),

]

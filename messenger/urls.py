from django.conf.urls import url

from . import views

urlpatterns = [
    url(r'^$', views.inbox, name='inbox'),
    url(r'^new/$', views.new, name='new_message'),
    url(r'^send/$', views.send, name='send_message'),
    url(r'^load_more/$', views.load_more, name='load_more'),
    url(r'^get_products/$', views.get_products, name='get_products'),
    url(r'^send_image/$', views.send_image, name='send_image'),
    url(r'^delete/$', views.delete, name='delete_message'),
    url(r'^users/$', views.users, name='users_message'),
    url(r'^check/$', views.check, name='check_message'),
    url(r'^add_new_messages/$', views.add_new_messages, name='add_new_messages'),
    url(r'^(?P<username>[^/]+)/$', views.messages, name='messages'),
]

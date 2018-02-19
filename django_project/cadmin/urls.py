from django.conf.urls import url, include
from . import views

urlpatterns = [
    url(r'^post/add/$', views.post_add, name='post_add'),
    url(r'^post/update/(?P<pk>[\d]+)/$', views.post_update, name='post_update'),
]
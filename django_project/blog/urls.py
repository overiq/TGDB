from django.conf.urls import url
from . import views

urlpatterns = [
    url(r'^category/(?P<category_slug>[\w-]+)/$', views.post_by_category, name='post_by_category'),
    url(r'^tag/(?P<tag_slug>[\w-]+)/$', views.post_by_tag, name='post_by_tag'),
    url(r'^(?P<pk>\d+)/$', views.post_detail, name='post_detail'),
    url(r'^$', views.post_list, name='post_list'),
]
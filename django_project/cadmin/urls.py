from django.conf.urls import url, include
from . import views
from django.contrib.auth import views as auth_views

urlpatterns = [
    url(r'^register/$', views.register, name='register'),
    url(r'^password-change-done/$',
        auth_views.password_change_done,
        {'template_name': 'cadmin/password_change_done.html'},
        name='password_change_done'
        ),
    url(r'^password-change/$',
        auth_views.password_change,
        {'template_name': 'cadmin/password_change.html' , 'post_change_redirect': 'password_change_done'},
        name='password_change'
        ),
    url(r'^$', views.home, name='home'),
    url(r'^login/$', views.login, {'template_name': 'cadmin/login.html'}, name='login'),
    url(r'^logout/$', auth_views.logout, {'template_name': 'cadmin/logout.html'}, name='logout'),
    url(r'^post/add/$', views.post_add, name='post_add'),
    url(r'^post/update/(?P<pk>[\d]+)/$', views.post_update, name='post_update'),
]
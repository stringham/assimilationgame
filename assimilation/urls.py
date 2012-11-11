from django.conf.urls.defaults import *
# from django.conf.urls import patterns, include, url

urlpatterns = patterns('assimilation.views',
    # Examples:
    # url(r'^$', 'game.views.home', name='home'),
    # url(r'^game/', include('game.foo.urls')),
    url(r'^home/$','index'),
    url(r'^games/$','games'),
    url(r'^auth/login/$', 'login'),
    url(r'^auth/logout/$', 'logout'),
    url(r'^auth/create/$', 'create'),

)



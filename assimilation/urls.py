from django.conf.urls.defaults import *
# from django.conf.urls import patterns, include, url

urlpatterns = patterns('assimilation.views',
    # Examples:
    # url(r'^$', 'game.views.home', name='home'),
    # url(r'^game/', include('game.foo.urls')),
    url(r'^home/$','index'),
    url(r'^games/$','games'),
    url(r'^play/(?P<id>[^/]+)$','play'),
    url(r'^makeadmin$','makeadmin'),
    url(r'^auth/login/$', 'login'),
    url(r'^auth/logout/$', 'logout'),
    url(r'^auth/create/$', 'create'),
    url(r'^chats/(?P<game_id>[^/]+)$','chats'),
    url(r'^usergames/$','usergames'),
    url(r'^game/create$','creategame'),
    url(r'^game/available$','availablegames'),
    url(r'^game/join/(?P<game_id>[^/]+)$','joingame'),
    url(r'^game/delete/(?P<game_id>[^/]+)$','deletegame'),
    url(r'^game/get/(?P<game_id>[^/]+)$','getgame'),
    url(r'^game/placetile/(?P<game_id>[^/]+)$','placetile'),

)



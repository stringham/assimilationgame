import settings
# from django.conf.urls import patterns, include, url
from django.conf.urls.defaults import *


# Uncomment the next two lines to enable the admin:
from django.contrib import admin
admin.autodiscover()

from django.conf.urls.defaults import *
from tastypie.api import Api 
from assimilation.api import *

v1_api = Api(api_name='v1')
v1_api.register(UserResource())
v1_api.register(GameResource())

game_resource = GameResource()

urlpatterns = patterns('',
    # Examples:
    # url(r'^$', 'game.views.home', name='home'),
    # url(r'^game/', include('game.foo.urls')),
    url(r'^assimilation/', include('assimilation.urls')),
    (r'^api/', include(v1_api.urls)),

    # Uncomment the admin/doc line below to enable admin documentation:
    url(r'^admin/doc/', include('django.contrib.admindocs.urls')),

    # Uncomment the next line to enable the admin:
    url(r'^admin/', include(admin.site.urls)),

    url(r'^favicon\.ico$', 'django.views.generic.simple.redirect_to', {'url':'assimilation/static/images/favicon.ico'}),
    url(r'^$', 'django.views.generic.simple.redirect_to', {'url':'assimilation/home'}),
)


urlpatterns += patterns('',
   (r'^assimilation/static/(?P<path>.*)$',
    'django.views.static.serve',
    {'document_root': settings.ROOT('assimilation/static/')})
   )
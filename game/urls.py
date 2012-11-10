import settings
from django.conf.urls import patterns, include, url

# Uncomment the next two lines to enable the admin:
from django.contrib import admin
admin.autodiscover()

urlpatterns = patterns('',
    # Examples:
    # url(r'^$', 'game.views.home', name='home'),
    # url(r'^game/', include('game.foo.urls')),
    url(r'^assimilation/', include('assimilation.urls')),

    # Uncomment the admin/doc line below to enable admin documentation:
    url(r'^admin/doc/', include('django.contrib.admindocs.urls')),

    # Uncomment the next line to enable the admin:
    url(r'^admin/', include(admin.site.urls)),

    url(r'^favicon\.ico$', 'django.views.generic.simple.redirect_to', {'url':'assimilation/static/images/favicon.ico'}),
)


urlpatterns += patterns('',
   (r'^assimilation/static/(?P<path>.*)$',
    'django.views.static.serve',
    {'document_root': settings.ROOT('assimilation/static/')})
   )
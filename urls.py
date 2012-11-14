from django.conf.urls.defaults import patterns, include, url
from django.conf import settings
from django.views import static

from main.views import *

from django.contrib import admin
admin.autodiscover()

urlpatterns = patterns('',
    url(r'^admin/', include(admin.site.urls)),
    url(r'^$', index, name='index'),
    url(r'^index/$', index, name='index'),
    url(r'^category/(?P<id>\d+)/$', category, name='category'),
    url(r'^category/(?P<id>\d+)/(?P<page>\d+)/$', category, name='category'),
    url(r'^product/(?P<id>\d+)/$', product, name='product'),
)

if settings.DEBUG:
    urlpatterns += patterns('',
        (r'^media/(?P<path>.*)$', static.serve, {'document_root': settings.MEDIA_ROOT}),
    )

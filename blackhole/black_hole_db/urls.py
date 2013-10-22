# -*- coding: utf-8 -*-
from django.conf.urls import patterns, include, url
from django.contrib.auth import views as django_views

# Uncomment the next two lines to enable the admin:
from django.contrib import admin
admin.autodiscover()

urlpatterns = patterns('',
    # Uncomment the admin/doc line below to enable admin documentation:
    url(r'^admin/doc/', include('django.contrib.admindocs.urls')),
    url(r'^login/$', django_views.login),
    url(r'^logout/$',django_views.logout,{'next_page': '/blackhole/index/'}),
    # Uncomment the next line to enable the admin:
    url(r'^admin/', include(admin.site.urls)),
#    url(r'^stats/$', 'black_hole_db.views.stats', name='stats'),
    url(r'^index/$', 'blackhole.black_hole_db.views.index', name='index'),
    url(r'^listUsers/$', 'blackhole.black_hole_db.views.listUsers', name='listUsers'),
    url(r'^listHosts/$', 'blackhole.black_hole_db.views.listHosts', name='listHosts'),
    url(r'^byUser/$', 'blackhole.black_hole_db.views.byUser', name='byUser'),
    url(r'^byHost/$', 'blackhole.black_hole_db.views.byHost', name='byHost'),
    url(r'^findSessionLog/$', 'blackhole.black_hole_db.views.findSessionLog', name='findSessionLog'),
    url(r'^getLog/(?P<log_id>\d+)$', 'blackhole.black_hole_db.views.get_log', name='getLog'),
)

from django.conf.urls import patterns, include, url

from django.contrib import admin
admin.autodiscover()

urlpatterns = patterns('',
    url(r'^$', 'home.views.index', name='index'),
    url(r'^transmission/', 'transmission.views.list', name='transmission'),
    url(r'^rpd/', 'rpd.views.index', name='rpd'),
    url(r'^league/', 'videoLeague.views.index', name='league'),
    url(r'^login/$', 'django.contrib.auth.views.login', name='login'),
    url(r'^logout/$', 'django.contrib.auth.views.logout', name='logout'),
    url(r'^accounts/', 'home.views.index'),
    url(r'^denied/', 'home.views.denied', name='denied'),
    url(r'^admin/', include(admin.site.urls)),
)
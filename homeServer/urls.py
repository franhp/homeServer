from django.conf.urls import patterns, include, url

# Uncomment the next two lines to enable the admin:
from django.contrib import admin
admin.autodiscover()

urlpatterns = patterns('',
    url(r'^$', 'home.views.index', name='index'),
    url(r'^transmission/', 'transmission.views.list', name='transmission'),
    url(r'^pyload/', 'pyload.views.list', name='pyload'),
    url(r'^jdownloader/', 'jdownloader.views.list', name='jdownloader'),
    url(r'^rpd/', 'rpd.views.index', name='rpd'),
    url(r'^login/$', 'django.contrib.auth.views.login', name='login'),
    url(r'^logout/$', 'django.contrib.auth.views.logout', name='logout'),
    url(r'^accounts/', 'home.views.index'),
    url(r'^denied/', 'home.views.denied', name='denied'),
    # Examples:
    # url(r'^$', 'homeServer.views.home', name='home'),
    # url(r'^homeServer/', include('homeServer.foo.urls')),

    # Uncomment the admin/doc line below to enable admin documentation:
    # url(r'^admin/doc/', include('django.contrib.admindocs.urls')),

    # Uncomment the next line to enable the admin:
    url(r'^admin/', include(admin.site.urls)),
)

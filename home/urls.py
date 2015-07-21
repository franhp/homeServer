from django.conf.urls import patterns, include, url

from django.contrib import admin
from django.contrib.auth.decorators import login_required
from home.views import HomeView
from random_video_downloader.views import VideoDownloaderView

from transmission.views import TransmissionView

admin.autodiscover()

urlpatterns = patterns('',
    url(r'^$', HomeView.as_view(), name='index'),
    url(r'^transmission/', login_required(
        TransmissionView.as_view()), name='transmission'),
   url(r'^downloader/', login_required(
        VideoDownloaderView.as_view()), name='downloader'),
    url(r'^login/$', 'django.contrib.auth.views.login', name='login'),
    url(r'^logout/$', 'django.contrib.auth.views.logout', name='logout'),
    url(r'^accounts/', HomeView.as_view()),
    url(r'^admin/', include(admin.site.urls)),
)
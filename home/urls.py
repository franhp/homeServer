from django.conf.urls import patterns, include, url

from django.contrib import admin
from django.contrib.auth.decorators import login_required
from games.views import RandomDirectoryCleanerView, LeagueView
from home.views import HomeView
from say.views import SayView
from smart_downloader.views import SmartDownloaderView
from video_downloader.views import VideoDownloaderView

from transmission.views import TransmissionView

admin.autodiscover()

urlpatterns = patterns('',
    url(r'^$', HomeView.as_view(), name='index'),
    url(r'^login/$', 'django.contrib.auth.views.login', name='login'),
    url(r'^logout/$', 'django.contrib.auth.views.logout', name='logout'),
    url(r'^accounts/', HomeView.as_view()),
    url(r'^admin/', include(admin.site.urls)),

    url(r'^say/', SayView.as_view(), name='say'),
    url(r'^downloader/', login_required(
        SmartDownloaderView.as_view()), name='smart-downloader'),
    url(r'^random_directory/', login_required(
        RandomDirectoryCleanerView.as_view()), name='random-directory'),
    url(r'^video_league/', login_required(
        LeagueView.as_view()), name='league'),
)
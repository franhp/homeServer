from django.conf.urls import patterns, include, url

from django.contrib import admin
from django.contrib.auth.decorators import login_required
from rest_framework.routers import DefaultRouter
from games.views import (
    RandomDirectoryCleanerView, LeagueView, SearchAndTagView, ShowVideoView,
    TagView, VideoView)
from home.views import HomeView
from say.views import SayView
from smart_downloader.views import SmartDownloaderView


admin.autodiscover()

router = DefaultRouter()
router.register(r'video_tags', TagView)
router.register(r'videos', VideoView)


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
    url(r'^video_search/', login_required(
        SearchAndTagView.as_view()), name='search-tag'),
    url(r'^show_video/(?P<video_id>[0-9]+)/$', login_required(
        ShowVideoView.as_view()), name='show-video'),
    url(r'^', include(router.urls)),
)

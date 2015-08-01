import os
import requests
from datetime import datetime

from django.conf import settings
from django.db import models
from pyquery import PyQuery
from youtube_dl import YoutubeDL


class VideoDownloader(models.Model):
    name = models.CharField(max_length=255)
    find_url_logic = models.TextField(blank=True, null=True)
    scheduled = models.BooleanField(default=False)
    output_dir = models.CharField(
        max_length=255, default=settings.DEFAULT_OUTPUT_DIR)
    last_execution = models.DateTimeField(null=True, blank=True)
    force = models.BooleanField(default=False)

    def __unicode__(self):
        return self.name

    def queue_download(self, title, url):
        self.downloads.create(title=title, video_url=url)

    def find_urls(self):
        """
        Must return a list of tuples containing (title, url)
        Can use requests or the pyquery library
        """
        urls = []
        assert requests and PyQuery  # Ensure dependencies are there
        exec self.find_url_logic
        return urls

    def queue_all(self):
        self.last_execution = datetime.now()
        self.force = False
        self.save()

        for title, url in self.find_urls():
            if not self._is_already_downloaded(url):
                self.queue_download(title, url)

    def _is_already_downloaded(self, video_url):
        return self.downloads.filter(video_url=video_url).exists()


class Video(models.Model):
    video_url = models.CharField(max_length=255)
    title = models.CharField(max_length=255)
    provider = models.ForeignKey(VideoDownloader, related_name='downloads')

    NOT_STARTED = 0
    STARTED = 1
    FINISHED = 2
    ERROR = 3
    STATUS_CHOICES = (
        (NOT_STARTED, 'Queued'),
        (STARTED, 'Started'),
        (FINISHED, 'Finished'),
        (ERROR, 'Error'),
    )
    status = models.IntegerField(choices=STATUS_CHOICES, default=NOT_STARTED)
    error = models.TextField(blank=True)
    updated_on = models.DateTimeField(auto_now=True)

    def __unicode__(self):
        return self.title

    def download(self):
        opts = {
            'outtmpl':
                os.path.join(
                    self.provider.output_dir, '%(title)s-%(id)s.%(ext)s'
                )
        }
        y = YoutubeDL(params=opts)

        self.status = self.STARTED
        self.save()

        try:
            y.download([self.video_url])
            self.status = self.FINISHED
        except Exception as e:
            self.error = e
            self.status = self.ERROR

        self.save()

    @staticmethod
    def list_downloads():
        return Video.objects.all().order_by('-updated_on')[:50]

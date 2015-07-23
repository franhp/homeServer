import os
from datetime import datetime

from django.conf import settings
from django.db import models
from pyquery import PyQuery
from youtube_dl import YoutubeDL


class VideoDownloader(models.Model):
    name = models.CharField(max_length=255)
    website = models.CharField(max_length=255, null=True, blank=True)
    element_query = models.TextField(blank=True)
    title_query = models.TextField(blank=True)
    url_query = models.TextField(blank=True)
    scheduled = models.BooleanField(default=False)
    output_dir = models.CharField(
        max_length=255, default=settings.DEFAULT_OUTPUT_DIR)
    last_execution = models.DateTimeField(null=True, blank=True)

    def __unicode__(self):
        return self.name

    def queue_download(self, title, url):
        self.downloads.create(title=title, video_url=url)

    def find_urls(self):
        urls = []
        html = PyQuery(url=self.website)
        elements = html(self.element_query)  # TODO doesn't work on all sites
        for element in elements:
            title = eval(self.title_query)
            url = eval(self.url_query)
            urls.append((title, url))
        return urls

    def queue_all(self):
        self.last_execution = datetime.now()
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

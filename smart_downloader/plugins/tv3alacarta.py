import os

from django.conf import settings

from youtube_dl import YoutubeDL

from smart_downloader.plugins import ProviderClass


class TV3Alacarta(ProviderClass):
    def match_pattern(self, file_url):
        return file_url.startswith('http://www.ccma.cat/')

    def find_title(self, url=None):
        return url.split('/')[-4:-3][0]

    def download(self, url=None, output=None):
        opts = {
            'outtmpl':
                os.path.join(
                    output, '%(title)s-%(id)s.%(ext)s'
                ),
            'progress_hooks': [self.progress_hook],
            'proxy': settings.DEFAULT_PROXY
        }
        y = YoutubeDL(params=opts)
        y.download([url])

    def downloaded_bytes(self, task=None):
        return task.result.get('current')

    def total_bytes(self, task=None):
        return task.result.get('total')

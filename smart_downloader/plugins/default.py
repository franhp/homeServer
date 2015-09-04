import os

from youtube_dl import YoutubeDL

from smart_downloader.plugins import ProviderClass


class DefaultProvider(ProviderClass):
    def find_title(self, url=None):
        return url[-15:]

    def match_pattern(self, file_url):
        return True

    def download(self, url=None, output=None):
        opts = {
            'outtmpl':
                os.path.join(
                    output, '%(title)s-%(id)s.%(ext)s'
                ),
            'progress_hooks': [self.progress_hook],
        }
        y = YoutubeDL(params=opts)
        y.download([url])

    def downloaded_bytes(self, task=None):
        return task.result.get('current')

    def total_bytes(self, task=None):
        return task.result.get('total')

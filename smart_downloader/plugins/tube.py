import os
from base64 import b64decode

from pyquery import PyQuery
from youtube_dl import YoutubeDL

from smart_downloader.plugins import ProviderClass


class ColouredTube(ProviderClass):
    encrypted_name = b64decode('aHR0cDovL3JlZHR1YmUuY29t')

    def match_pattern(self, file_url):
        return file_url.startswith(self.encrypted_name)

    def find_more_links(self, data=None):
        html = PyQuery(data.provider_url)
        elements = html('span.video-title')
        urls = []
        for element in elements:
            title = element.xpath('a/@title')[0]
            url = self.encrypted_name + element.xpath('a/@href')[0]
            urls.append((title, url))
        return urls

    def find_title(self, url=None):
        pq = PyQuery(url=url)
        return pq('title').text()

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

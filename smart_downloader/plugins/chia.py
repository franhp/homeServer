import os

from pyquery import PyQuery
from youtube_dl import YoutubeDL

from smart_downloader.plugins import ProviderClass


class ChiaProvider(ProviderClass):
    def match_pattern(self, file_url):
        return file_url.startswith('http://www.chia-anime.tv/')

    def find_more_links(self, data=None):
        pq = PyQuery(url=data.provider_url)
        urls = []
        for url in pq('.post')[:5]:
            p = PyQuery(url=url.xpath('div/a/@href')[0])
            vid = p('#download')
            urls.append((vid.text(), vid.attr('href')))
        return urls

    def find_title(self, url=None):
        return url.split('/')[-2:-1]

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

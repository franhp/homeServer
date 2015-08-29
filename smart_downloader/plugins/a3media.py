# -*- coding: utf-8 -*-
import os

import requests
from pyquery import PyQuery
from celery import current_task
from youtube_dl import YoutubeDL

from smart_downloader.plugins import ProviderClass


class A3Media(ProviderClass):
    def find_more_links(self, data=None):
        response = requests.get(data.provider_url + 'carousel.json')
        found_links = []
        for element in response.json()['1']:
            found_links.append(
                (
                    data.provider_name + ' ' + element['title'],
                    element['hrefHtml']
                )
            )
        return found_links

    def progress_hook(self, d):
        current_task.update_state(
            state='PROGRESS',
            meta={'current': d['downloaded_bytes'], 'total': d['total_bytes']}
        )

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

    def match_pattern(self, file_url):
        return file_url.startswith('http://www.atresplayer.com/')

    def find_title(self, url=None):
        pq = PyQuery(url=url)
        return pq('title').text().replace(u'Volver a ver vídeos de', '')

    def downloaded_bytes(self, task=None):
        return task.result.get('current')

    def total_bytes(self, task=None):
        return task.result.get('total')

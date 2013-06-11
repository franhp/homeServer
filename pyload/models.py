from django.db import models
from django.conf import settings
import requests
import json

class pyloadClient(models.Model):
    class Meta:
            permissions = (('can_pyload', 'Can enter the pyload section'),)

    session = ''
    url = 'http://%s:%s/api/' % (settings.PYLOAD_HOSTNAME, settings.PYLOAD_PORT)

    def __init__(self):
        params = {'username': settings.PYLOAD_USERNAME, 'password': settings.PYLOAD_PASSWORD}
        self.session = requests.post(self.url + 'login', data=params, headers={}).text[1:-1]

    def request_post(self, url, data=None):
        params = {'session': self.session}
        if data is not None:
            for k, v in data.items():
                data[k] = json.dumps(v)
            params.update(data)
        return requests.post(self.url+url, data=params).text

    def getDownloads(self):
        return json.loads(self.request_post('statusDownloads'))

    def getQueue(self):
        return json.loads(self.request_post('getQueueData'))

    def addLink(self, url):
        url = 'http://'+url if not url.startswith('http://') else url
        self.request_post('addPackage', data={'name': 'homeServer', 'links': [url]})

    def deleteFinished(self):
        self.request_post('deleteFinished');

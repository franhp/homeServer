from django.db import models
import requests
import xmltodict


class jdownloaderClient(models.Model):
    class Meta:
            permissions = (('can_jdownloader', 'Can enter the jdownloader section'),)

    def __init__(self, hostname, port):
        self.base_url = 'http://%s:%s' % (hostname, port)

    def getQueue(self):
        return xmltodict.parse(requests.get(self.base_url+'/get/downloads/alllist').text)

    def addLink(self, url):
        url = 'http://'+url if not url.startswith('http://') else url
        return requests.get(self.base_url+'/action/add/links/grabber0/start1/'+url).text

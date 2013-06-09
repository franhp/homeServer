from django.db import models
from django.conf import settings
import transmissionrpc

class transmissionClient(models.Model): 
    class Meta:
            permissions = (('can_transmission', 'Can enter the transmission section'),)

    tc = ''

    def __init__(self):
        self.tc = transmissionrpc.Client(settings.TRANSMISSION_HOST, port=settings.TRANSMISSION_PORT)

    def getTorrents(self):
        return self.tc.get_torrents()

    def addTorrent(self, url):
        return self.tc.add_torrent(url)

    def delTorrent(self, torrent_hash):
        return self.tc.remove_torrent(torrent_hash)

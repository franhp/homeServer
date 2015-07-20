from django.db import models
from django.conf import settings
import transmissionrpc


class TransmissionClient(models.Model):
    @staticmethod
    def get_torrents():
        tc = transmissionrpc.Client(
            settings.TRANSMISSION_HOST, port=settings.TRANSMISSION_PORT)
        return tc.get_torrents()

    @staticmethod
    def add_torrent(url):
        tc = transmissionrpc.Client(
            settings.TRANSMISSION_HOST, port=settings.TRANSMISSION_PORT)
        return tc.add_torrent(url)

    @staticmethod
    def del_torrent(torrent_hash):
        tc = transmissionrpc.Client(
            settings.TRANSMISSION_HOST, port=settings.TRANSMISSION_PORT)
        return tc.remove_torrent(torrent_hash)

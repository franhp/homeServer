from django.conf import settings
import transmissionrpc

from smart_downloader.plugins import ProviderClass


class TransmissionProvider(ProviderClass):
    def __init__(self):
        self.tc = transmissionrpc.Client(
            settings.TRANSMISSION_HOST, port=settings.TRANSMISSION_PORT)

    def match_pattern(self, file_url):
        return (file_url.endswith('.torrent')
                or file_url.startswith('magnet:?'))

    def download(self, url=None, output=None):

        obj = self.tc.add_torrent(url)
        return obj._fields['hashString'].value

    def update_fields(self, task):
        # TODO monitor all torrents instead of just the task one
        from smart_downloader.models import File
        obj = File.objects.filter(task__task_id=task.task_id)[0]
        for torrent in self.tc.get_torrents():
            if torrent._fields['hashString'].value == task.result:
                obj.title = torrent._fields['name'].value
                obj.save()

                if torrent._fields['leftUntilDone'].value is 0:
                    task.status = 'SUCCESS'
                    task.save()
                else:
                    task.status = 'PROGRESS'
                    task.meta = {
                        'current': torrent._fields['totalSize'].value - torrent._fields['leftUntilDone'].value,
                        'total': torrent._fields['totalSize'].value
                    }
                    task.save()
                return
        task.status = 'SUCCESS'
        task.save()

    def downloaded_bytes(self, task=None):
        return task.meta.get('current')

    def total_bytes(self, task=None):
        return task.meta.get('total')

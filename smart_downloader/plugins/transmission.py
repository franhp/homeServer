from django.conf import settings
from django.db.models.query_utils import Q
from djcelery.models import TaskMeta
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

    def update_fields(self):
        from smart_downloader.models import File

        ids_to_ignore = []
        for torrent in self.tc.get_torrents():
            hash_string = torrent._fields['hashString'].value
            title = torrent._fields['name'].value

            # Filter doesn't work with PickledObjectField so ...
            for f in File.objects.all():
                if f.task.result == hash_string:
                    obj = f
                    break
                obj = None

            if obj:
                ids_to_ignore.append(obj.id)

                if obj.title != title:
                    obj.title = title
                    obj.save()

                task = obj.task
                if torrent._fields['leftUntilDone'].value is 0:
                    task.status = 'SUCCESS'

                else:
                    task.status = 'PROGRESS'
                    task.meta = {
                        'current': (torrent._fields['totalSize'].value
                                    - torrent._fields['leftUntilDone'].value),
                        'total': torrent._fields['totalSize'].value
                    }

                task.save()

            else:
                # Other torrents added manually through the client
                task = TaskMeta.objects.create(task_id=title,
                                               status='STARTED',
                                               result=hash_string)
                new_file = File.objects.create(
                    title=title,
                    file_url=torrent._fields['torrentFile'].value,
                    task=task)
                ids_to_ignore.append(new_file.id)


        # Other torrents in our database no longer present on client
        qs = (
            Q(file_url__endswith='.torrent') | Q(file_url__startswith='magnet:?')
        )
        other_torrents = File.objects.filter(qs).exclude(id__in=ids_to_ignore)
        for t in other_torrents:
            t.task.status = 'SUCCESS'
            t.task.save()

    def downloaded_bytes(self, task=None):
        return task.meta.get('current')

    def total_bytes(self, task=None):
        return task.meta.get('total')
